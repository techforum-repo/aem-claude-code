---
description: Rules for AEM Content Fragment models, fragments, and GraphQL persisted queries
paths:
  - "ui.content/**/settings/dam/cfm/**/*.xml"
  - "ui.content/**/content/dam/**/*.xml"
  - "ui.config/**/graphql/**/*.json"
  - "core/src/main/**/*ContentFragment*.java"
  - "core/src/main/**/*CF*.java"
---

# Content Fragments and headless rules

## Content Fragment models

- Define CF models under `/conf/<project>/settings/dam/cfm/models/` — never under `/content`
- Model definition XML must be placed in `ui.content` — models are mutable, not immutable
- Every field must have a `fieldLabel` and a stable `name` — changing `name` breaks existing fragments
- Use `required` sparingly — required fields block fragment creation in workflows
- Fragment variations must be accounted for in any consuming code

## GraphQL persisted queries

- Store persisted queries under `/conf/<project>/settings/graphql/persistedQueries/`
- Always use persisted queries in production — ad-hoc queries are disabled by Dispatcher in AEMaaCS
- Never expose sensitive content paths or JCR structure details in query responses
- Paginate large result sets — use `limit` and `cursor`-based pagination

## Java / Sling Model integration

- Adapt `Resource` to `ContentFragment` using `resource.adaptTo(ContentFragment.class)` — null-check the result
- Use `ContentFragment.getElement(name)` to access fields — handle `null` when the element does not exist
- Never adapt `SlingHttpServletRequest` to `ContentFragment` directly
- Use the `AssetManager` or `FragmentTemplate` API for programmatic fragment creation, not manual JCR writes

## Headless delivery

- All headless endpoints must go through the AEM GraphQL servlet — never expose raw JCR APIs
- Dispatcher must allow `/graphql/execute.json/*` for persisted query execution
- CORS configuration must be in `ui.config` — not hardcoded in servlet filters
- Test CF model changes against existing fragments before deploying — field renames are breaking changes

## Review focus

- Are CF model changes backward-compatible with existing fragments?
- Are persisted queries used rather than ad-hoc queries?
- Is pagination applied to queries that could return large result sets?
- Are `adaptTo(ContentFragment.class)` results null-checked?
- Is CORS configured via OSGi in `ui.config`?
