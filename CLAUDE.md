# AEM Claude Code Guidance

This repository contains an Adobe Experience Manager as a Cloud Service (AEMaaCS) project. Apply AEM package boundaries, Cloud Manager safety rules, and existing module conventions before suggesting or generating changes.

## Module structure

- `core/`
  Sling Models, OSGi services, servlets, schedulers, workflow steps, and shared Java logic
- `ui.apps/`
  AEM components, dialogs, HTL, clientlibs, and immutable `/apps` content
- `ui.apps.structure/`
  Repository structure definitions that must install before `ui.apps`
- `ui.content/`
  Mutable content, editable templates, policies, and experience/content structure
- `ui.config/`
  OSGi configurations, service user mappings, and Repoinit scripts
- `ui.frontend/`, `ui.frontend.react/`, `ui.frontend.spa/`
  Distinct frontend modules with different integration patterns
- `all/`
  Aggregation package that embeds deployable modules
- `it.tests/`
  Integration tests — run by Cloud Manager after deployment against a live AEM environment
- `ui.tests/`
  UI tests — run by Cloud Manager against the publish environment using browser automation

## Build commands

- Full build: `mvn clean install`
- Deploy to author: `mvn clean install -PautoInstallPackage -Daem.host=localhost -Daem.port=4502`
- Deploy to publish: `mvn clean install -PautoInstallPackage -Daem.host=localhost -Daem.port=4503`
- Build without tests: `mvn clean install -DskipTests`
- Run tests only: `mvn test`
- Format code: `mvn spotless:apply`

## Java version

This project targets **Java 21**. Prefer Java 21 language features in all new and modified code:
- **Records** for immutable value objects and DTOs instead of manual classes with constructors, getters, and `equals`/`hashCode`
- **Pattern matching for `instanceof`** — use `instanceof Foo f` instead of casting after a type check
- **Text blocks** for multi-line strings such as JCR-SQL2 queries and JSON templates
- **Switch expressions** (`->` syntax) instead of statement switches with `break`
- **`var`** for local variable type inference where the type is obvious from the right-hand side
- **Sealed classes** to restrict Sling Model or service hierarchies where extension should be controlled

## Core rules

- Prefer Sling Models for component-backed presentation logic and OSGi services for reusable business logic.
- Keep business logic out of HTL.
- Place OSGi configuration and Repoinit in `ui.config`, not `ui.apps`.
- Keep `ui.apps` immutable and keep mutable content in `ui.content`.
- Use service users for repository access; never use admin `ResourceResolver` or `loginAdministrative`.
- Always close `ResourceResolver` and `Session` objects correctly.
- Never call `Thread.sleep()` in servlets, jobs, schedulers, or workflow steps.
- Use SLF4J parameterized logging only; do not use `System.out`, `System.err`, or string concatenation in log calls.
- Ensure JCR queries are indexed, bounded, and not executed in tight rendering loops.
- Follow existing patterns in the same module before introducing new abstractions or structures.

## Change guidance

- Keep changes minimal, scoped, and aligned with the owning module.
- Call out assumptions for non-trivial work.
- Mention Cloud Manager, OakPAL, Dispatcher, or SonarCloud risks when they are relevant.
- Suggest validation steps or tests when logic, rendering, configuration, or packaging changes.

## Claude Code configuration

- **Rules** — `.claude/rules/` files activate automatically based on `paths:` patterns when you read or edit matching files.
- **Commands** — `.claude/commands/` provides five entry-point commands, invoked as `/project:<command-name>`.
- **Skills** — `.claude/skills/` provides focused, reusable review skills. Invocable directly (e.g. `/aem-security`, `/aem-cloudmanager`); `/project:review` spawns dedicated reviewer agents in parallel instead.
- **Hooks** — `.claude/hooks/guard-sensitive-files.py` blocks edits to credential files. Registered in `.claude/settings.json`.
- **Permissions** — `.claude/settings.json` defines allow / ask / deny tiers for shell commands.
- **Personal overrides** — `.claude/settings.local.json` (git-ignored) for per-developer permission additions.
- **LSP** — `jdtls-lsp` and `typescript-lsp` plugins are enabled in `settings.json`. When the language server binaries are on PATH, Claude gets real-time diagnostics, go-to-definition, find references, and type information after every edit. See README for install steps (jdtls is not available via apt/brew — manual install required).
