#!/usr/bin/env python3
"""
PostToolUse hook: after Claude writes or edits a Java file,
auto-run mvn spotless:apply on the core module to keep formatting consistent.
"""
import json
import os
import shutil
import subprocess
import sys

def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    # Only act on Write or Edit tool calls
    tool = payload.get("tool_name", "")
    if tool not in ("Write", "Edit"):
        sys.exit(0)

    # Only act on Java files
    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".java"):
        sys.exit(0)

    # Only act on core module files
    if "/core/src/" not in file_path and "\\core\\src\\" not in file_path:
        sys.exit(0)

    mvn_cmd = shutil.which("mvn") or "/usr/local/bin/mvn" or "/opt/homebrew/bin/mvn"
    if not shutil.which("mvn") and not os.path.isfile(mvn_cmd):
        print(f"[post-format] mvn not found — skipping Spotless for {file_path}", file=sys.stderr)
        sys.exit(0)

    try:
        result = subprocess.run(
            [mvn_cmd, "spotless:apply", "-pl", "core", "-q"],
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ}
        )
        if result.returncode == 0:
            print(f"[post-format] Spotless applied to {file_path}")
        else:
            print(f"[post-format] Spotless failed for {file_path}:\n{result.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print(f"[post-format] mvn not found on PATH — skipping Spotless for {file_path}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print(f"[post-format] Spotless timed out for {file_path} — skipping", file=sys.stderr)

    sys.exit(0)

if __name__ == "__main__":
    main()
