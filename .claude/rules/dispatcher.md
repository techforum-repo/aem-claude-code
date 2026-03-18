---
description: Rules for Dispatcher configuration — security filters, caching, Cloud Manager compatibility
paths:
  - "devops/**/*.conf"
  - "devops/**/*.any"
  - "devops/**/*.vhost"
  - "devops/**/*.farm"
---

# Instructions for Dispatcher configuration

## Scope
Use this guidance for Dispatcher configuration that affects security, caching, and Cloud Manager compatibility.

## Key rules
- `/filter` should default deny; allow only explicitly required paths.
- Block or tightly restrict sensitive AEM endpoints such as `/crx`, `/system`, `/bin/wcmcommand`, `/bin/receive`, `/etc/replication`, `/mnt/overlay`, `/editor.html`, and Content Fragment authoring/editor routes (for example `/assets.html` and `/mnt/overlay/dam/cfm`).
- Restrict `.json` and especially `.infinity.json` exposure unless a specific public use case exists.
- Ensure required security headers are present where the repository manages them.
- Never cache authenticated, personalized, or user-specific responses.
- Use `/ignoreUrlParams` to avoid unnecessary cache fragmentation from analytics-style query parameters.
- Keep cache invalidation rules aligned with actual publish flush behavior.
- Use only Dispatcher directives supported by the AEMaaCS Dispatcher SDK.

## Review focus
- default-deny filter posture
- exposure of sensitive endpoints or JSON data
- security header coverage
- caching of authenticated or personalized content
- Dispatcher SDK and Cloud Manager compatibility
