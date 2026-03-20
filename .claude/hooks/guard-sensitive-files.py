#!/usr/bin/env python3
"""
PreToolUse hook: block edits to files that likely contain secrets or credentials.
Works on Windows, Linux, and macOS without additional dependencies.
Exit code 2 = block the action and show the message to the user.
"""
import json
import os
import sys

data = json.load(sys.stdin)
file_path = data.get("tool_input", {}).get("file_path", "")

if not file_path:
    sys.exit(0)

name = os.path.basename(file_path).lower()

SENSITIVE_PATTERNS = [
    ".env",
    "credentials",
    "secret",
    "password",
    "keystore",
    ".jks",
    ".p12",
    ".pfx",
    ".key",
]

for pattern in SENSITIVE_PATTERNS:
    if pattern in name:
        print(json.dumps({
            "decision": "block",
            "reason": f"Blocked: '{file_path}' matches a sensitive file pattern ('{pattern}'). Edit it manually if this is intentional.",
        }))
        sys.exit(2)

sys.exit(0)
