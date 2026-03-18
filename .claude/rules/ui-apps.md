---
description: Rules for ui.apps — AEM components, dialogs, HTL, clientlibs, immutable /apps content
paths:
  - "ui.apps/**/*.html"
  - "ui.apps/**/*.xml"
  - "ui.apps/**/*.js"
  - "ui.apps/**/*.css"
  - "ui.apps/**/*.scss"
---

# Instructions for `ui.apps`

## Scope
Use this guidance for AEM components, dialogs, HTL, clientlib definitions, and other immutable application content under `ui.apps`.

## Key rules
- Keep business logic out of HTL; use Sling Models or services for computed values.
- Preserve placeholders, edit mode behavior, and authoring usability.
- Maintain backward compatibility in dialogs where possible; renamed or removed fields can break existing authored content.
- Use HTL output contexts correctly:
  - never use `${var @ context='unsafe'}`
  - use `context='uri'` for URLs and actions
  - use `context='html'` only for trusted, sanitized HTML
  - use `context='scriptString'` inside script blocks
- Keep `ui.apps` immutable: no `/content` paths, no mutable editable-template content under `/conf`, and no OSGi configs here.
- Avoid `rep:policy` or `authorizable` nodes unless explicitly reviewed.

## Review focus
- business logic leaking into HTL
- broken authoring behavior or placeholders
- backward-incompatible dialog changes
- incorrect HTL output context usage
- mutable content or OSGi config placed in `ui.apps`
