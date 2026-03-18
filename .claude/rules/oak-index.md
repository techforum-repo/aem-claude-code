---
description: Rules for Oak index definitions — index type selection, property coverage, and Cloud Manager safety
paths:
  - "ui.apps/**/oak:index/**/*.xml"
  - "ui.apps/**/_oak_index/**/*.xml"
  - "ui.content/**/oak:index/**/*.xml"
---

# Oak index rules

## Index type selection

- Use **`lucene`** indexes for full-text search and complex property queries
- Use **`property`** indexes only for exact-match lookups on a single property with low cardinality
- Never use `traversal` — it scans the whole repository and will degrade under load
- Prefer extending an existing index over creating a new one

## Required properties on every index

- `jcr:primaryType` must be `oak:QueryIndexDefinition`
- `type` must be set (`lucene` or `property`)
- `async` should be `async` (or `async,nrt` for near-real-time) — synchronous indexing blocks writes
- `evaluatePathRestrictions` must be `true` if queries use path restrictions (`ISDESCENDANTNODE`)

## Lucene index rules

- Every indexed property needs an explicit `propertyDefinition` node with `name` and `propertyIndex` or `analyzed`
- Set `nodeScopeIndex=true` only if full-text search across node content is needed — it is expensive
- Include only the `nodeTypes` your query targets — indexing all node types is wasteful
- Add `tags` to match the index to the specific query using `option(index tag ...)`

## Property index rules

- Only index properties with low cardinality (few distinct values)
- Set `unique=true` if the property is unique — this enables faster equality lookups
- Do not index high-cardinality properties (e.g. `jcr:lastModified`, UUIDs) with a property index

## Review focus

- Does the index cover all properties and node types used in the corresponding query?
- Is `evaluatePathRestrictions` set when the query uses path-based restrictions?
- Is `async` set — synchronous indexes block JCR writes?
- Does the index name follow the project convention (e.g. `myproject-product-lucene`)?
- Is the index placed in `ui.apps` (for application indexes) and embedded in `all/`?
