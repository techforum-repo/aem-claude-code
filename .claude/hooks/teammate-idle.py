#!/usr/bin/env python3
"""
TeammateIdle hook: fires when a reviewer teammate is about to go idle.
Checks if the teammate has produced a findings report — if not, sends
feedback to keep them working.
"""
import json
import sys


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    teammate_name = payload.get("teammate_name", "")
    last_message = payload.get("last_message", "")

    review_keywords = ["blocking", "warning", "suggestion", "finding", "no issues"]

    # A real findings report needs both a keyword and enough content to be substantive.
    # A very short last_message (< 150 chars) almost certainly isn't a complete report
    # even if it accidentally contains a keyword like "no issues".
    has_keyword = any(kw in last_message.lower() for kw in review_keywords)
    has_report = has_keyword and len(last_message.strip()) >= 150

    if not has_report:
        print(
            f"[teammate-idle] {teammate_name} has not yet produced a findings report. "
            "Complete your review and report all findings as Blocking / Warning / Suggestion before finishing.",
            file=sys.stderr
        )
        sys.exit(2)  # Exit code 2 keeps the teammate working

    sys.exit(0)


if __name__ == "__main__":
    main()
