---
description: Rules for ui.config — OSGi configurations, service user mappings, Repoinit scripts
paths:
  - "ui.config/**/*.xml"
---

# Instructions for `ui.config`

## Scope
Use this guidance for OSGi configurations, service user mappings, and Repoinit scripts in `ui.config`.

## Key rules
- Place OSGi configs here, not in `ui.apps`.
- Use valid AEM runmode folder names such as `config`, `config.author`, `config.publish`, `config.dev`, `config.stage`, and `config.prod`.
- Ensure config file names match the OSGi PID exactly, including factory PID `~identifier` naming.
- Do not hardcode secrets, tokens, or environment-specific confidential values.
- Keep service user mappings and Repoinit here, with least-privilege access design.

## Review focus
- incorrect module placement for config files
- invalid runmode folder names
- PID and filename mismatch
- hardcoded secrets
- overly broad service user permissions
