---
description: Rules for the all aggregation package — embed order, filter roots, OakPAL safety
paths:
  - "all/**/*.xml"
---

# Instructions for the `all` module

## Scope
The `all` module is the aggregation package. Changes here affect packaging, installation order, and deployment safety across the whole AEM application.

## Key rules
- Preserve the correct embed order: `ui.apps.structure` → `ui.apps` → `ui.content` and `ui.config`.
- Do not add or remove embedded packages unless the change explicitly requires it.
- Do not add filter roots in `all` for paths already owned by embedded sub-packages.
- Avoid overlapping filter roots across embedded packages; these cause OakPAL violations and unpredictable installs.
- Review any filter or embed change for content deletion risk during install or upgrade.

## Review focus
- embed order correctness
- missing embeds after adding a module
- overlapping filter roots
- filter changes that could delete or overwrite existing content unexpectedly
