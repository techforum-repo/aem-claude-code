---
description: Rules for WCM Core Components — proxy components, dialog inheritance, allowedComponents, clientlib categories, versioning
paths:
  - "ui.apps/**/.content.xml"
  - "ui.apps/**/*.html"
  - "ui.content/**/policies/**"
  - "ui.content/**/templates/**"
  - "core/**/pom.xml"
  - "pom.xml"
---

# Instructions for WCM Core Components

## Proxy components

- **Always create proxy components** — never copy Core Component HTL, Java, or dialog files into your project. Copies diverge from upstream and miss security patches.
- A proxy component's `.content.xml` must set `sling:resourceSuperType` to the versioned Core Component path, e.g.:
  ```xml
  sling:resourceSuperType="core/wcm/components/text/v3/text"
  ```
- The proxy component node should contain **only** what you are overriding — no unnecessary copies of inherited files.
- When overlaying a Core Component dialog, extend it via `sling:resourceSuperType` on the `cq:dialog` node rather than copying the full dialog XML. Full copies break when the upstream dialog changes.

## Component versioning

- Pin the Core Components version in the root `pom.xml` via `core.wcm.components.version` property. Do not use `LATEST` — it causes non-reproducible builds.
- When upgrading Core Components, check the [release notes](https://github.com/adobe/aem-core-wcm-components/releases) for breaking HTL or dialog changes before applying.
- Prefer the latest stable major version (v3/v4) for new proxy components. Do not mix versions of the same component type across a project.

## allowedComponents and policies

- After creating any new component, add it to the relevant editable template's `allowedComponents` policy in `ui.content`. A deployed component that is not in the allowed list cannot be placed by authors.
- Policies live under `/conf/<project>/settings/wcm/policies/` in `ui.content`. The `components` property lists allowed `sling:resourceType` values.
- Do not hardcode component paths in policies — use the project's `sling:resourceType` base path consistently.

## Clientlib categories

- Core Components rely on specific clientlib categories being present. Do not remove or rename categories inherited from Core Components:
  - `core.wcm.components.commons.v1` — shared utilities
  - `core.wcm.components.commons.datalayer.v1` — Adobe Client Data Layer (ACDL)
- If your project uses ACDL, ensure `core.wcm.components.commons.datalayer.v1` is loaded on every page. Missing this breaks analytics integrations silently.
- Custom clientlib categories must not conflict with Core Component category names.

## Content Fragment and Experience Fragment components

- Use the Core Component CF display (`core/wcm/components/contentfragment/v1/contentfragment`) for rendering CFs on pages — do not build custom renderers unless the use case cannot be met by the Core Component.
- XF components (`core/wcm/components/experiencefragment/v1/experiencefragment`) require the XF path to be set in the component policy, not the dialog, to allow template-level reuse.

## Review focus

- Component copying Core Component HTL or Java instead of using a proxy
- `sling:resourceSuperType` missing or pointing to a non-existent or deprecated version
- New components not added to `allowedComponents` in the relevant template policy
- Core Components version not pinned in `pom.xml`
- ACDL clientlib category missing from page clientlib includes
- Dialog copied in full instead of extended via `sling:resourceSuperType`
