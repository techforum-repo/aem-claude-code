---
description: Baseline rules for all Java files in the core module — Sling Models, OSGi services, servlets, schedulers, workflow steps
paths:
  - "core/src/main/**/*.java"
---

# Instructions for Java files in `core`

## Scope
Applies to all Java source files in `core`: Sling Models, OSGi services, servlets, filters, schedulers, and workflow steps.

Three rules apply simultaneously to `core/src/main/**/*.java`: this file, `core-java-security.md`, and `core-java-performance.md`. When guidance overlaps, follow the strictest rule.

## Java 21 features

This project targets Java 21. Use these features in new and modified code:
- **Records** — for immutable value objects (e.g. search result items, DTOs) instead of manual classes with constructors, getters, `equals`, and `hashCode`
- **Pattern matching for `instanceof`** — `if (resource instanceof ValueMap vm)` instead of cast-after-check
- **Text blocks** — for multi-line JCR-SQL2 queries and JSON templates
- **Switch expressions** — `->` syntax instead of statement switches with `break`
- **`var`** — for local variable type inference where the type is clear from context
- **Sealed classes** — to restrict model or service hierarchies where arbitrary extension should be prevented

Do not introduce Java 21 features into code that will not be compiled at Java 21 source level (`<maven.compiler.release>21</maven.compiler.release>` in `core/pom.xml`).

## Key rules
- Prefer Sling Models for component-backed presentation logic and OSGi services for shared or reusable business logic.
- Follow existing package structure, annotation style, injection patterns, and naming conventions used by nearby classes.
- Reuse existing helpers and utilities before introducing new abstractions.
- Never use admin `ResourceResolver` or `loginAdministrative`; use a service user when repository access is needed.
- Always close `ResourceResolver` and `Session` objects in all code paths.
- Never call `Thread.sleep()` in servlets, jobs, schedulers, or workflow steps.
- Use SLF4J parameterized logging only.
- Avoid deprecated AEM, Sling, or JCR APIs.

## WCM Core Components delegation
If the implementation extends a WCM Core Component, use the delegation pattern:
- inject the delegate with `@Self @Via(type = ResourceSuperType.class)`
- override only the behavior that differs
- do not reimplement inherited logic unnecessarily

## OSGi event handlers

Use `EventHandler` for reacting to repository or OSGi framework events:
- Register with `@Component(service = EventHandler.class)` and `@EventHandlerProperty` for the topic filter
- Keep handler execution fast — offload slow work to a `JobManager` job, never block the event thread
- Use `JobConsumer` (via `JobManager.addJob()`) instead of `EventHandler` when the work must be reliable, retryable, or distributed across cluster nodes
- Never use `EventHandler` for content replication — use `ReplicationContentFilter` or a workflow instead
- Unregister cleanly — `@Deactivate` must cancel any pending async work started by the handler

## Review focus
- unsafe resolver or session usage
- missing cleanup for `ResourceResolver` or `Session`
- deprecated API usage
- `Thread.sleep()` or other request-blocking behavior
- poor reuse or unnecessary abstraction
- missing or weak tests for non-trivial logic
