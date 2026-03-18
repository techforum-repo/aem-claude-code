---
description: Rules for ui.frontend.react — React bundles integrated into AEM-rendered experiences
paths:
  - "ui.frontend.react/**/*.js"
  - "ui.frontend.react/**/*.jsx"
  - "ui.frontend.react/**/*.ts"
  - "ui.frontend.react/**/*.tsx"
  - "ui.frontend.react/**/*.css"
  - "ui.frontend.react/**/*.scss"
---

# Instructions for `ui.frontend.react`

## Scope
Use this guidance for React-based frontend bundles that integrate into AEM-rendered experiences but are not the full SPA module.

## Key rules
- Follow the React conventions already used in this module.
- Do not mix in `ui.frontend.spa` routing or SPA editor patterns unless the module already uses them.
- Preserve existing props, model/data contracts, and AEM integration points.
- Explain any impact on authored content, rendered markup, or clientlib loading when relevant.

## Review focus
- accidental mixing of SPA-only patterns
- breaking props or backend data contracts
- hidden assumptions about AEM markup or authored content
