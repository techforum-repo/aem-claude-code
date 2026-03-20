# Claude Code request cheatsheet

Five commands cover everything. Skills can be chained or run standalone.

**Commands** (invoked as `/project:command-name`):
- `/project:review` — comprehensive review — creates a native agent team with four specialist reviewers (security, performance, Cloud Manager, SonarCloud) running in parallel, then consolidates findings
- `/project:create` — any AEM artifact, detects type automatically
- `/project:explain` — component walkthrough or pipeline impact
- `/project:pr` — PR summary with risks and test plan
- `/project:bug` — bug investigation

**Skills** (invoked directly by name):
- `/aem-security` — security-only check
- `/aem-performance` — performance-only check
- `/aem-cloudmanager` — Cloud Manager / OakPAL check
- `/aem-sonar` — SonarCloud quality check
- `/aem-oak-index` — Oak index review or creation
- `/aem-headless` — Content Fragments and GraphQL review

Rules in `.claude/rules/` activate automatically when Claude reads or edits matching files — no action needed.

---

## Review

### Full review of current branch changes
```
/project:review
```
*(runs `git diff`, spawns four reviewer agents in parallel — security, performance, Cloud Manager, SonarCloud — then merges all findings into one report)*

### Review specific file(s)
```
/project:review core/src/main/java/com/example/models/ProductModel.java
```

### Quick focused checks (single skill)
```
/aem-security core/src/main/java/com/example/servlets/ProductServlet.java
```
```
/aem-cloudmanager
```
*(checks current diff for OakPAL and deployment risks only)*

```
/aem-sonar core/src/main/java/com/example/services/impl/ProductServiceImpl.java
```

### Security-focused review
```
Review my current changes for service user usage, HTL XSS context, admin resolver usage, and sensitive data exposure.
```

### Review for JCR query and performance issues
```
Review this file for unindexed queries, queries in render paths, unbounded result sets, and ResourceResolver lifecycle issues:
[file path]
```

---

## Create

### Create any AEM artifact (component, model, service, servlet, scheduler, repoinit, test, frontend)
```
/project:create
[describe what you need — Claude detects the type automatically]
```

**Examples:**
```
/project:create
A product card component with title, image, price, and CTA link. Dialog with style system variants for dark/light backgrounds.
```
```
/project:create
Sling Model for the product card component at apps/myproject/components/product-card
```
```
/project:create
OSGi service that fetches product data from an external API, with configurable endpoint URL
```
```
/project:create
Sling Servlet that returns product JSON at /api/products, read-only, no JCR access needed
```
```
/project:create
Scheduler that runs nightly to clean up expired session nodes under /content/usergenerated
```
```
/project:create
Repoinit for a service user that reads /content/mysite and writes /content/usergenerated
```
```
/project:create
Unit tests for core/src/main/java/com/example/models/ProductModel.java
```
```
/project:create
React component for the product card in ui.frontend.react, consuming the product card model JSON
```
```
/project:create
Oak index for a JCR-SQL2 query that selects product nodes by sku property under /content/mysite
```
```
/project:create
Content Fragment model for a product with title, description, price, and image fields
```
```
/project:create
CAConfig interface for site-specific API endpoint URL and timeout settings
```
```
/project:create
Dispatcher vhost for mysite.com with SSL termination and caching rules
```
```
/project:create
i18n dictionary for the product card component in English and German
```
```
/project:create
Editable template for a product landing page with header, content, and footer structure
```
```
/project:create
Overlay for /libs/cq/gui/components/coral/common/tabs to add a custom tab to the page properties dialog
```
```
/project:create
Integration test that verifies the product card component renders correctly on publish
```
```
/project:create
UI test using Cypress that checks an author can create and publish a product page
```
```
/project:create
OSGi EventHandler that listens for DAM asset ingestion events and triggers cache invalidation
```
```
/project:create
OSGi config for the product API service using Cloud Manager environment variable for the endpoint URL and a secret for the API key
```

---

## Explain

### Explain a component end to end
```
/project:explain ui.apps/src/main/content/jcr_root/apps/myproject/components/product-card
```
```
/project:explain com.example.models.ProductModel
```

### Analyse Cloud Manager pipeline impact of current changes
```
/project:explain
```
*(no argument — uses `git diff main...HEAD` to identify what changed)*

### Explain a file or service
```
Explain this file in the context of the repository and its related modules:
core/src/main/java/com/example/services/impl/ProductServiceImpl.java
```

### Trace impact before changing something
```
Trace where this component or service is used and what could break if I change it:
[file or folder path]
```

---

## PR and release

### Draft PR summary
```
/project:pr
```
*(runs `git diff main...HEAD` and `git log` automatically)*

### Draft testing notes
```
Draft reviewer notes and testing notes for this change:
[file or folder path]
```

### Risks and rollback
```
Summarize implementation risks, deployment impact, and rollback considerations for this change:
[file or folder path]
```

---

## Bug investigation

### Investigate a bug
```
/project:bug
[brief bug description — include what was expected, what happened, and on which environment]
```
```
/project:bug
The product card shows a blank title on publish but works on author. No errors in logs.
```

### Compare two implementations
```
Compare these two implementations and tell me which better fits repository conventions, AEM best practices, and maintainability:
- [file path 1]
- [file path 2]
```

---

## Git and diff workflows

### Summarize current changes
```
Summarize the modified files and their purpose in the context of this AEM repository.
```

### Generate a commit message
```
Suggest a concise git commit message for my current staged changes.
```

### What could break
```
What existing behavior could break from my current changes? Focus on AEM authoring impact, package filters, and downstream dependencies.
```

---

## Quality and security

### Null safety and complexity check
```
Review this file for null safety, exception handling, deeply nested logic, and the smallest practical cleanups:
[file path]
```

### Test gap review
```
Review this change and tell me what unit tests or integration tests are missing:
[file or folder path]
```

---

## Oak indexes

### Review an existing index
```
/aem-oak-index ui.apps/src/main/content/jcr_root/oak:index/myproject-product-lucene/.content.xml
```

### Create an index for a specific query
```
/aem-oak-index
Create an Oak index for: SELECT * FROM [nt:unstructured] WHERE ISDESCENDANTNODE('/content/mysite') AND [sling:resourceType] = 'myproject/components/product' AND [sku] IS NOT NULL
```

---

## Content Fragments and headless

### Review a CF model or GraphQL query
```
/aem-headless ui.content/src/main/content/jcr_root/conf/mysite/settings/dam/cfm/models/product
```

### Check headless delivery setup
```
/aem-headless
Review our headless setup for persisted query configuration, CORS policy, and Dispatcher filter rules.
```

---

## Dispatcher and configuration

### Review Dispatcher configuration
```
Review this Dispatcher configuration for default-deny filters, sensitive path exposure, cache rules, and Cloud Manager SDK compatibility:
[dispatcher config file path]
```

### Review OSGi configuration
```
Review this OSGi config for correct runmode folder, PID filename, and hardcoded secrets:
[ui.config file path]
```

---

## Understanding and onboarding

### Onboard to an area of the codebase
```
Help me understand this area of the repository, the main files involved, and what to inspect next:
[folder path]
```

### Safe refactoring in an isolated worktree
```
Refactor this Sling Model to extract the query logic into a dedicated OSGi service:
core/src/main/java/com/example/models/ProductModel.java
```
*(Claude delegates to the `aem-refactor` agent — runs in an isolated git worktree so your branch is untouched until you review and merge the changes)*

```
Rename ProductService to CatalogService across core, ui.config, and any HTL references.
```

---

## Bulk operations with /batch

Run the same task across many files in parallel:

### Apply a naming convention fix across all Sling Models
```
/batch
For each file matching core/src/main/java/**/models/**/*.java, check whether the @Model annotation includes defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL and add it if missing.
```

### Add missing null checks across all servlets
```
/batch
For each file matching core/src/main/java/**/servlets/**/*.java, check for unguarded resource.adaptTo() calls and add null checks where missing.
```

### Migrate log statements to parameterized format
```
/batch
For each Java file in core/src/main, replace any log statements using string concatenation with SLF4J parameterized format.
```

---

## Polling with /loop

Re-run a check on an interval until a condition is met:

### Poll Cloud Manager pipeline status
```
/loop 5m
Check if the Cloud Manager pipeline at [pipeline URL] has finished. If it has failed, summarize the failure reason. Stop when it reaches succeeded or failed status.
```

### Watch for test failures after a change
```
/loop 2m
Run mvn test -pl core -q and report if any tests fail. Stop after the first clean run.
```

---

## LSP code intelligence (Java and TypeScript)

LSP support is active when `jdtls-lsp` (Java) and `typescript-lsp` (TypeScript) plugins are installed and enabled in `.claude/settings.json`. Claude uses hover, go-to-definition, and diagnostics automatically when reading or editing code.

### Test that LSP is active
```
What is the return type of SlingHttpServletRequest.getResource()?
```
*(If LSP is working, Claude uses `lsp_hover` — visible in tool calls. If it falls back to Grep/Read, jdtls is still indexing.)*

### Go to definition
```
Where is ResourceResolverFactory defined and what does the getServiceResourceResolver method signature look like?
```

### Find all usages of a service
```
Find all places where ProductService is injected or used across the codebase.
```

### Check for compile errors before committing
```
Check core/src/main/java/com/example/models/ProductModel.java for any type errors or unresolved references.
```

### Inspect an interface before implementing it
```
Show me the full interface definition for WorkflowProcess so I can implement it correctly.
```

### Review a method signature before calling it
```
What parameters does QueryBuilder.createQuery() accept and what does it return?
```

> **Note:** jdtls indexes the Maven workspace on first run — this takes 3–5 minutes. During indexing, Claude falls back to Grep/Read. Once indexing is complete, `lsp_hover` and `lsp_get_document_symbols` appear in tool calls confirming LSP is active.

---

## Plan mode (read-only exploration before edits)

Enable plan mode before large refactors to let Claude explore without touching any files:

- **CLI**: `claude --permission-mode plan`
- **VS Code**: `Shift+Tab` twice in the chat input to toggle plan/auto mode

### Use case: explore before a large refactor
```
[enter plan mode]
Map all the files I would need to change to rename ProductService to CatalogService across core, ui.config, and any HTL references.
[review the plan, then exit plan mode to execute]
```

### Use case: understand impact before touching a filter
```
[enter plan mode]
What filter roots in ui.content would be affected if I change the filter mode on /content/mysite/us from merge to replace?
```
