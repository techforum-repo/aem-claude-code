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
- Do not run expensive queries or resource traversal inside `@PostConstruct` for frequently rendered Sling Models.
- Prefer lazy initialization when data may not always be needed.
- Do not store request, resolver, or session state in OSGi service instance fields.
- Keep resolver and session lifetime as short as possible.

## Review focus
- unbounded or non-indexed queries
- query execution inside loops
- heavy work in `@PostConstruct`
- long-lived resolver or session usage
- request-scoped state stored in singleton services
