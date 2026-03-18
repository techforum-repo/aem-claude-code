---
description: Rules for ui.frontend.spa — AEM SPA module with SPA Editor, model JSON, and component mapping
paths:
  - "ui.frontend.spa/**/*.js"
  - "ui.frontend.spa/**/*.jsx"
  - "ui.frontend.spa/**/*.ts"
  - "ui.frontend.spa/**/*.tsx"
  - "ui.frontend.spa/**/*.css"
  - "ui.frontend.spa/**/*.scss"
---

# Instructions for `ui.frontend.spa`

## Scope
Use this guidance for the AEM SPA module that depends on AEM model JSON, SPA component mapping, and SPA Editor integration.

## Key rules
- Follow the existing SPA architecture and conventions used in this module.
- Preserve routing, component mapping, and AEM SPA Editor integration points.
- Keep contracts between AEM model JSON and React components explicit.
- Explain authored-content impact when changing mapping, routes, page containers, or data expectations.

## Review focus
- broken model mapping or routing behavior
- regressions in SPA Editor integration
- hidden authored-content or JSON contract changes
