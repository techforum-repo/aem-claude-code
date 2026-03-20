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
import tempfile
import time

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

    # Only act on core module files — normalize separators first to handle
    # mixed paths on Windows (e.g. C:\project/core/src/Foo.java from Git Bash)
    file_path_norm = file_path.replace("\\", "/")
    if "/core/src/" not in file_path_norm:
        sys.exit(0)

    # Debounce: skip if Spotless was already run in the last 30 seconds.
    # Claude often edits multiple Java files in quick succession; running mvn
    # for each edit would be slow. One run per 30-second window is enough.
    debounce_file = os.path.join(tempfile.gettempdir(), "aem_spotless_last_run")
    now = time.time()
    try:
        with open(debounce_file) as f:
            last_run = float(f.read().strip())
        if now - last_run < 30:
            sys.exit(0)
    except (OSError, ValueError):
        pass
    with open(debounce_file, "w") as f:
        f.write(str(now))

    # Works on Windows (mvn.cmd), Linux, and macOS as long as mvn is on PATH
    mvn_cmd = shutil.which("mvn") or shutil.which("mvn.cmd")
    if not mvn_cmd:
        sys.exit(0)

    try:
        result = subprocess.run(
            [mvn_cmd, "spotless:apply", "-pl", "core", "-q"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
            env={**os.environ}
        )
        if result.returncode == 0:
            print(json.dumps({"decision": "approve", "reason": f"Spotless applied to {file_path}"}))
        else:
            print(json.dumps({"decision": "block", "reason": f"Spotless failed for {file_path}:\n{result.stderr}"}))
    except FileNotFoundError:
        sys.exit(0)
    except subprocess.TimeoutExpired:
        sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()
