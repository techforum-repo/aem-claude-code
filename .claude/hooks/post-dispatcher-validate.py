#!/usr/bin/env python3
"""
PostToolUse hook: after Claude writes or edits a Dispatcher config file,
auto-run the AEM Dispatcher SDK validator to catch config errors immediately.

Requires the AEM Dispatcher Tools SDK to be installed. The validator binary
is looked up on PATH first, then at standard AEM SDK install locations.
Skips gracefully if the validator is not found.

Platform notes:
  - Linux/macOS: binary is named 'validator' (Go binary, no extension); hook expects a
                 symlink at ~/aem-sdk/bin/validate pointing to it
  - Windows:     binary is named 'validator.exe' (or 'validate.cmd')
"""
import json
import os
import shutil
import subprocess
import sys


def respond(decision, reason):
    print(json.dumps({"decision": decision, "reason": reason}))
    sys.exit(0)

# Dispatcher config file extensions that trigger validation
DISPATCHER_EXTENSIONS = (".any", ".conf", ".rules", ".vars", ".farm", ".vhost")

# Path fragments — file must be under one of these to trigger validation
DISPATCHER_PATH_FRAGMENTS = (
    "conf.dispatcher.d",
    "conf.d",
    "dispatcher/src",
    "dispatcher\\src",
)


def is_dispatcher_file(file_path):
    path_norm = file_path.replace("\\", "/").lower()
    if not any(frag.replace("\\", "/") in path_norm for frag in DISPATCHER_PATH_FRAGMENTS):
        return False
    return any(file_path.lower().endswith(ext) for ext in DISPATCHER_EXTENSIONS)


def find_validator():
    """
    Locate the AEM Dispatcher SDK validator binary.

    Search order:
      1. PATH — 'validate' (Linux/macOS) or 'validator.exe' (Windows)
      2. Standard AEM SDK install locations (Linux/macOS and Windows)
    """
    is_windows = sys.platform == "win32"

    # Check PATH — Adobe ships the binary as 'validator' on Linux/macOS (Go binary)
    # and also as a 'validate' shell-script wrapper in older SDK versions.
    for name in (["validator.exe"] if is_windows else ["validate", "validator"]):
        found = shutil.which(name)
        if found:
            return found

    # Standard SDK fallback locations (if not on PATH).
    # Covers both the legacy dispatcher/bin/ layout and the current flat bin/ layout.
    # ~/aem-sdk/bin/validate is the recommended symlink target (created manually or by install).
    unix_candidates = [
        os.path.expanduser("~/aem-sdk/bin/validate"),
        os.path.expanduser("~/aem-sdk/bin/validator"),
        os.path.expanduser("~/aem-sdk/dispatcher/bin/validate"),
        os.path.expanduser("~/aem-sdk/dispatcher/bin/validator"),
    ]
    win_candidates = [
        os.path.expanduser("~/aem-sdk/bin/validator.exe"),
        os.path.expanduser("~/aem-sdk/bin/validate.cmd"),
        os.path.expanduser("~/aem-sdk/dispatcher/bin/validator.exe"),
    ]

    candidates = win_candidates if is_windows else unix_candidates
    for candidate in candidates:
        if os.path.isfile(candidate):
            return candidate

    return None


def find_dispatcher_src(file_path):
    """
    Walk up from the edited file to find the dispatcher src root —
    the directory that contains conf.dispatcher.d/.
    This is the argument passed to the validator.
    """
    path = os.path.abspath(file_path)
    while True:
        parent = os.path.dirname(path)
        if parent == path:
            break
        path = parent
        if os.path.isdir(os.path.join(path, "conf.dispatcher.d")):
            return path
    return None


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        sys.exit(0)

    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not is_dispatcher_file(file_path):
        sys.exit(0)

    validator = find_validator()
    if not validator:
        print(
            f"[post-dispatcher-validate] AEM Dispatcher SDK validator not found — skipping.\n"
            "Install the Dispatcher Tools from the AEM SDK zip, then symlink the binary:\n"
            "  Linux/macOS: ln -sf ~/aem-sdk-*/dispatcher-sdk-*/bin/validator ~/aem-sdk/bin/validate\n"
            "  Windows:     ~/aem-sdk/bin/validator.exe  or  ~/aem-sdk/bin/validate.cmd\n"
            "Note: validate.cmd and validator.exe are Windows-only and will not run on Linux.",
            file=sys.stderr,
        )
        sys.exit(0)

    dispatcher_src = find_dispatcher_src(file_path)
    if not dispatcher_src:
        print(
            f"[post-dispatcher-validate] Could not locate dispatcher src root (conf.dispatcher.d/) "
            f"from {file_path} — skipping.",
            file=sys.stderr,
        )
        sys.exit(0)

    try:
        # The validator is invoked as: validate full <path-to-dispatcher-src>
        # 'full' validates both httpd and dispatcher configuration files.
        # dispatcher-src is the directory containing conf.dispatcher.d/
        result = subprocess.run(
            [validator, "full", dispatcher_src],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            env={**os.environ},
        )
        if result.returncode == 0:
            respond("approve", f"Dispatcher validation passed for {file_path}")
        else:
            output = (result.stdout + result.stderr).strip()
            respond("block", f"Dispatcher validation FAILED for {file_path}:\n{output}")
    except FileNotFoundError:
        respond("approve", f"Validator binary not executable — skipping for {file_path}")
    except subprocess.TimeoutExpired:
        respond("approve", f"Validator timed out — skipping for {file_path}")


if __name__ == "__main__":
    main()
