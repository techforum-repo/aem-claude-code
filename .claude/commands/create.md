---
description: Create any AEM artifact — component, Sling Model, OSGi service, servlet, scheduler, workflow step, Repoinit, Oak index, Content Fragment model, CAConfig, Dispatcher config, i18n keys, unit test, or frontend code
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Write, Edit, Bash(mvn *), Bash(mvn clean*)
argument-hint: "[artifact type and description, e.g. 'Sling Model for product card']"
---

Create: $ARGUMENTS

Detect the artifact type from the request and apply the appropriate creation approach:

| If the request mentions | Create |
|---|---|
| component, dialog, HTL | AEM component across `core` (Sling Model) + `ui.apps` (HTL + dialog) + `ui.content` (template/policy if needed) |
| Sling Model, model | Sling Model in `core` |
| OSGi service, service | OSGi service in `core` |
| servlet | Sling Servlet in `core` |
| scheduler, job, JobConsumer | OSGi Scheduler or Sling Job in `core` |
| workflow, process step | Workflow process step in `core` |
| repoinit, service user, ACL | Repoinit script + service user mapping in `ui.config` |
| Oak index, JCR index, query index | Oak index definition XML in `ui.apps/oak:index/` — apply `aem-oak-index` skill rules |
| Content Fragment model, CF model | CF model definition XML in `ui.content` under `/conf/<project>/settings/dam/cfm/models/` |
| GraphQL, persisted query | Persisted query JSON under `/conf/<project>/settings/graphql/persistedQueries/` |
| CAConfig, context-aware config | `@Configuration` interface in `core` + config node in `ui.content` under `/conf/<project>/sling:configs/` |
| Dispatcher, vhost, farm, rewrite | Dispatcher config files in `devops/dispatcher/` — apply `dispatcher` rule |
| i18n, translation, dictionary | i18n JSON files in `ui.apps/<project>/i18n/` for each required language |
| unit test, test | Unit tests in `core/src/test` |
| frontend, React, clientlib, SPA | Frontend code in the correct frontend module |

Before writing code:
1. **Find existing examples** — use Glob and Grep to locate 1-2 existing files of the same artifact type in the project (e.g. another Sling Model, another OSGi service, another HTL component). If none exist, use the closest artifact type as reference.
2. **Extract the pattern** — from the example(s), note: package declaration, imports, annotations and their attributes, class/interface naming convention, injection style (`@ValueMapValue` vs `@Inject`), logging setup, and any project-specific base classes or interfaces.
3. **Check for existing implementations** — search for a class or component that already does something similar before creating a new one.
4. **Identify all modules touched** — list every module that needs a change (e.g. a new Sling Model also needs a service user in `ui.config` and may need a dialog in `ui.apps`).
5. **Ask one clarifying question** if the type or scope is genuinely ambiguous — otherwise proceed.

Requirements:
- Follow existing package structure, annotation style, and naming conventions
- Keep business logic in Java (Sling Models / OSGi services), not in HTL
- Use service users for repository access — never admin `ResourceResolver`
- Always close `ResourceResolver` and `Session` with try-with-resources
- Never call `Thread.sleep()` in servlets, jobs, schedulers, or workflow steps
- Call out any required `ui.content`, `ui.config`, or `all/` changes
- Suggest tests for non-trivial logic

Output:
1. What will be created — modules and files
2. Code
3. Validation steps
