---
description: Rules for ui.apps.structure — repository structure definitions, installation order prerequisite
paths:
  - "ui.apps.structure/**/*.xml"
---

# Instructions for `ui.apps.structure`

## Scope
This module defines repository structure that must exist before `ui.apps` installs.

## Key rules
- Treat structure changes as installation-order-sensitive.
- Do not modify structure definitions without understanding the affected repository paths and package dependencies.
- Keep this module aligned with its role as a prerequisite package in `all`.

## Review focus
- structure changes that break package installation order
- unnecessary structure additions
- path ownership conflicts with other modules
