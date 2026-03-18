---
description: Unit test rules for core Java tests — AemContext, Mockito, meaningful assertions
paths:
  - "core/src/test/**/*.java"
---

# Instructions for Java test files in `core`

## Scope
Use this guidance for unit tests covering Sling Models, OSGi services, utilities, and other Java behavior in the `core` module.

## Key rules
- Follow the test framework and class structure already used in nearby tests.
- Use `AemContext` for Sling Model tests and component-backed behavior.
- Use `@ExtendWith(MockitoExtension.class)` when no AEM context is required.
- Test meaningful behavior, not only mock wiring.
- Cover primary paths, null handling, and meaningful edge cases.
- Keep each test focused on one behavior with clear assertions.

## Review focus
- tests that only prove mock setup
- missing assertions
- missing null or edge-case coverage
- unnecessary `AemContext` usage
- brittle tests that over-mock simple collaborators
