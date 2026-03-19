---
description: Performance rules for Java files in core — queries, traversal, resolver lifecycle, PostConstruct
paths:
  - "core/src/main/**/*.java"
---

# Performance instructions for Java files in `core`

## Scope
Apply these rules when reviewing or generating Java code that reads the repository, renders page data, or runs in request or background execution paths.

## Key rules
- Ensure every JCR query is backed by an Oak index and has an explicit limit when appropriate.
- Do not execute queries inside loops.
- Avoid broad tree traversal when a targeted query or direct lookup is more appropriate.
- When iterating over a large number of child nodes, prefer the JCR Node API (`node.getNodes()`) over the Sling API (`resource.listChildren()`) — the JCR API uses a lazy cursor and avoids loading all children into memory at once.
- Do not run expensive queries or resource traversal inside `@PostConstruct` for frequently rendered Sling Models.
- Prefer lazy initialization when data may not always be needed.
- Do not store request, resolver, or session state in OSGi service instance fields.
- Keep resolver and session lifetime as short as possible.
- Always close `ResourceResolver` and `Session` using try-with-resources or a `finally` block — never rely on GC. Both implement `Closeable`; prefer `try (ResourceResolver resolver = ...) { }` to guarantee closure on all paths including exceptions.

## Review focus
- unbounded or non-indexed queries
- query execution inside loops
- heavy work in `@PostConstruct`
- long-lived resolver or session usage
- resolver or session not closed via try-with-resources or finally
- Sling `listChildren()` used for large child node iteration instead of JCR `node.getNodes()`
- request-scoped state stored in singleton services
