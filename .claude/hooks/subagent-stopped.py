#!/usr/bin/env python3
"""
SubagentStopped hook: fires when a reviewer teammate stops before finishing.
Checks if the teammate produced a complete findings report — if not, warns
the lead context that a review domain is missing from the final report.
Exit code 2 tells Claude Code the teammate should be restarted.
"""
import json
import sys

REVIEWER_TEAMMATES = {
    "security-reviewer",
    "performance-reviewer",
    "cloudmanager-reviewer",
    "sonar-reviewer",
    "maintainability-reviewer",
    "accessibility-reviewer",
}

COMPLETION_KEYWORDS = ["blocking", "warning", "suggestion", "finding", "no issues"]


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    teammate_name = payload.get("teammate_name", "")
    last_message = payload.get("last_message", "")

    # Only act on known reviewer teammates
    if teammate_name not in REVIEWER_TEAMMATES:
        sys.exit(0)

    has_keyword = any(kw in last_message.lower() for kw in COMPLETION_KEYWORDS)
    has_report = has_keyword and len(last_message.strip()) >= 150

    if not has_report:
        print(
            f"\n[review] WARNING: {teammate_name} stopped before producing a findings report.\n"
            f"The final review will be INCOMPLETE — the {teammate_name.replace('-reviewer', '')} "
            f"domain was not covered.\n"
            f"Restarting {teammate_name} to complete the review.",
            file=sys.stderr,
        )
        sys.exit(2)  # Exit code 2 restarts the teammate

    sys.exit(0)


if __name__ == "__main__":
    main()
