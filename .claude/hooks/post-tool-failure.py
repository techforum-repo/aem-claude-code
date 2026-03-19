#!/usr/bin/env python3
"""
PostToolUseFailure hook: log tool failures with context to help diagnose
recurring issues with Maven builds, formatting, or file operations.
"""
import json
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool = payload.get("tool_name", "unknown")
    error = payload.get("error", "")

    # Only surface actionable failures
    if tool == "Bash":
        cmd = payload.get("tool_input", {}).get("command", "")
        print(f"[tool-failure] Bash command failed: {cmd}\nReason: {error}", file=sys.stderr)
    elif tool in ("Write", "Edit"):
        file_path = payload.get("tool_input", {}).get("file_path", "")
        print(f"[tool-failure] {tool} failed on: {file_path}\nReason: {error}", file=sys.stderr)
    else:
        print(f"[tool-failure] {tool} failed\nReason: {error}", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
