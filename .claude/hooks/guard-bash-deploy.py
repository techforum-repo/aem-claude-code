#!/usr/bin/env python3
"""
PreToolUse hook: block Maven auto-install commands targeting non-localhost AEM instances.
Prevents Claude from accidentally deploying to shared dev, staging, or production environments.
Exit code 2 = block the action and show the message to the user.
"""
import json
import os
import re
import sys

# Hosts that are safe to deploy to without confirmation
LOCALHOST_VALUES = {"localhost", "127.0.0.1", "::1"}

# AEM_HOST env var — if set, used as the default deploy target
DEFAULT_HOST = os.environ.get("AEM_HOST", "localhost")


def extract_aem_host(command: str) -> str | None:
    """
    Extract the value of -Daem.host=<value> from a Maven command string.
    Returns None if the flag is not present (meaning the default host is used).
    """
    match = re.search(r"-Daem\.host=([^\s]+)", command)
    return match.group(1) if match else None


def is_autoinstall_command(command: str) -> bool:
    """True if the command includes the autoInstallPackage or autoInstallBundle profile."""
    return bool(re.search(r"-P[^\s]*autoInstall", command))


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool = payload.get("tool_name", "")
    if tool != "Bash":
        sys.exit(0)

    command = payload.get("tool_input", {}).get("command", "")

    # Only inspect Maven commands with an autoInstall profile
    if "mvn" not in command or not is_autoinstall_command(command):
        sys.exit(0)

    # Determine the target host — explicit flag overrides env default
    host = extract_aem_host(command)
    effective_host = host if host is not None else DEFAULT_HOST

    if effective_host.lower() not in LOCALHOST_VALUES:
        print(
            f"Blocked: Maven autoInstall targeting '{effective_host}' (non-localhost).\n"
            f"Claude may only deploy to localhost. Run this command manually if intentional:\n"
            f"  {command}",
            file=sys.stderr,
        )
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
