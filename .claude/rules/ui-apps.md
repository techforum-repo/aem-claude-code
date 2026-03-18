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

## Overlays

Overlays customise OOTB AEM or WCM Core Component behavior by mirroring a `/libs/` path under `/apps/`:

- Mirror the `/libs/` path exactly under `/apps/` — e.g. `/libs/cq/gui/components/foo` → `/apps/cq/gui/components/foo`
- Copy only the files you need to change — do not copy the entire component tree
- Set `sling:resourceSuperType` to the original `/libs/` path on the overlay node to inherit unmodified behavior
- Prefer `sling:resourceSuperType` delegation over full overlays where possible — overlays block AEM upgrades from patching the original
- Never overlay `/libs/` files for logic that could be implemented as an OSGi service or Sling Model
- Test overlays after every AEM SDK upgrade — the overlaid `/libs/` file may have changed

## Review focus
- business logic leaking into HTL
- broken authoring behavior or placeholders
- backward-incompatible dialog changes
- incorrect HTL output context usage
- mutable content or OSGi config placed in `ui.apps`
- overlay copying more `/libs/` files than necessary
- overlay missing `sling:resourceSuperType` back to `/libs/`
