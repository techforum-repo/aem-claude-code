#!/usr/bin/env python3
"""
PostToolUse hook: after Claude writes or edits a Dispatcher config file,
auto-run the AEM Dispatcher SDK validator to catch config errors immediately.

Requires the AEM Dispatcher Tools SDK to be installed. The validator binary
is looked up on PATH first, then at standard AEM SDK install locations.
Skips gracefully if the validator is not found.

Platform notes:
  - Linux/macOS: binary is named 'validate' (shell script)
  - Windows:     binary is named 'validator.exe'
"""
import json
import os
import shutil
import subprocess
import sys

# Dispatcher config file extensions that trigger validation
DISPATCHER_EXTENSIONS = (".any", ".conf", ".rules", ".vars", ".farm")

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

    # Check PATH
    for name in (["validator.exe", "validate.cmd"] if is_windows else ["validate"]):
        found = shutil.which(name)
        if found:
            return found

    # Standard SDK fallback location (if not on PATH)
    unix_candidates = [
        os.path.expanduser("~/aem-sdk/dispatcher/bin/validate"),
    ]
    win_candidates = [
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
            "Install the Dispatcher Tools from the AEM SDK and ensure the binary is on PATH.\n"
            "  Linux/macOS: ~/aem-sdk/dispatcher/bin/validate\n"
            "  Windows:     ~/aem-sdk/dispatcher/bin/validator.exe",
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
        # The validator is invoked as: validate <path-to-dispatcher-src>
        # where dispatcher-src is the directory containing conf.dispatcher.d/
        result = subprocess.run(
            [validator, dispatcher_src],
            capture_output=True,
            text=True,
            timeout=30,
            env={**os.environ},
        )
        if result.returncode == 0:
            print(f"[post-dispatcher-validate] Validation passed for {file_path}")
        else:
            output = (result.stdout + result.stderr).strip()
            print(
                f"[post-dispatcher-validate] Validation FAILED for {file_path}:\n{output}",
                file=sys.stderr,
            )
    except FileNotFoundError:
        print(
            f"[post-dispatcher-validate] Validator binary not executable — skipping for {file_path}",
            file=sys.stderr,
        )
    except subprocess.TimeoutExpired:
        print(
            f"[post-dispatcher-validate] Validator timed out for {file_path} — skipping",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
