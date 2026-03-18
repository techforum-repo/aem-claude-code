---
description: Rules for ui.content — mutable content, templates, policies, experience fragments, content XML
paths:
  - "ui.content/**/*.xml"
---

# Instructions for `ui.content`

## Scope
Use this guidance for mutable content, templates, policies, experience fragments, and other content/package XML under `ui.content`.

## Key rules
- Keep `ui.content` limited to mutable content and configuration that belongs with content ownership.
- Do not place immutable application paths such as `/apps` or `/libs` here.
- Avoid `rep:policy`, `authorizable`, `/oak:index`, `/home`, or `/libs` content unless explicitly required and reviewed.
- Review non-default filter modes such as `merge` or `replace` carefully because they can alter existing authored content during install.
- Avoid overlapping filter roots with other embedded packages in `all`.

## Editable templates

- Store editable templates under `/conf/<project>/settings/wcm/templates/<template-name>/`
- Every template requires: `jcr:content` (template definition), `structure/` (locked structure), `policies/` (policy mappings), `initial/` (initial content)
- Set `status` to `enabled` only when the template is ready for authoring — leave as `draft` during development
- `allowedPaths` on the template policy controls which pages can use the template — scope it tightly
- Allowed components are controlled via policy, not template structure — place policy mappings in `policies/`
- Never copy `/libs/` template structure directly — extend via `sling:resourceSuperType`

## Review focus
- mutable versus immutable path separation
- ACL or authorizable content in packages
- filter mode changes with upgrade risk
- unintended impact on existing authored content
- editable template `status` left as `draft` unintentionally
- template `allowedPaths` too broad
