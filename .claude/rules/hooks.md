---
description: Rules for hooks — local developer workflow scripts, commit and validation hooks
paths:
  - "hooks/**/*"
---

# Instructions for `hooks`

## Scope
These scripts affect local developer workflow, commit behavior, and local validation flow.

## Key rules
- Keep behavior predictable and easy to explain.
- Call out any change that affects commit, push, validation, or local setup flow.
- Avoid surprising side effects or destructive behavior in local workflow scripts.

## Review focus
- unexpected workflow changes
- fragile local assumptions
- developer experience regressions
