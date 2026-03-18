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

## Cloud Manager environment variables and secrets

Use Cloud Manager variable substitution syntax in `.cfg.json` files — never hardcode environment-specific values:

```json
{
  "endpoint.url": "$[env:API_ENDPOINT;default=https://api.example.com]",
  "api.timeout": "$[env:API_TIMEOUT;default=5000]",
  "api.key": "$[secret:API_KEY]"
}
```

- `$[env:VAR_NAME]` — resolved from Cloud Manager environment variables; use `default=` for local dev fallback
- `$[secret:SECRET_NAME]` — resolved from Cloud Manager secret variables; never use `default=` on secrets
- Secrets are write-only in Cloud Manager — never log or expose them in responses
- Provide a `.cfg.json` with `default=` values that work for local AEM SDK development
- Document all required CM variables in a `README` or runbook — they must be set before deployment

## Review focus
- incorrect module placement for config files
- invalid runmode folder names
- PID and filename mismatch
- hardcoded secrets or environment-specific URLs
- missing `default=` on env vars (breaks local dev)
- `default=` on secrets (security risk)
- overly broad service user permissions
