---
description: Comprehensive AEM code review — spawns security, performance, Cloud Manager, and SonarCloud reviewer agents in parallel, then consolidates all findings into one report
context: fork
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git diff), Bash(git status), Bash(git log *)
argument-hint: "[file or class path, or leave blank to review current branch diff]"
---

Review: $ARGUMENTS

If no path is provided, run `git diff` to identify what changed in the current branch.

## Step 1 — Spawn all four reviewer agents in parallel

Delegate to all four agents simultaneously, passing the same target (`$ARGUMENTS`, or the git diff output if no argument):

- **`aem-security-reviewer`** — admin resolver, query injection, path validation, hardcoded secrets, servlet exposure
- **`aem-performance-reviewer`** — JCR queries, traversal, resolver lifecycle, PostConstruct overhead, threading
- **`aem-cloudmanager-reviewer`** — OakPAL violations, embed order, Dispatcher SDK, deployment safety
- **`aem-sonar-reviewer`** — complexity, duplication, null safety, resource leaks, security hotspots

Each agent runs in its own isolated context and returns its findings independently.

## Step 2 — Inline checks (run in this context while agents are working)

5. **Module placement** — are changes in the correct module? immutable (`ui.apps`) vs mutable (`ui.content`, `ui.config`) path separation?
6. **HTL** — output context on every expression, no logic in HTL, backward-compatible dialog field changes
7. **Resource lifecycle** — `ResourceResolver` and `Session` closed in all code paths?
8. **Tests** — meaningful assertions, null and edge-case coverage, no brittle mock-only tests?

## Step 3 — Consolidate and report

Merge all agent findings with the inline checks into one report:

1. **Summary** — what was reviewed and scope
2. **All findings** — consolidated and deduplicated, labelled **Blocking** / **Warning** / **Suggestion**, grouped by domain (Security / Performance / Cloud Manager / Quality / Structure)
3. **Recommended fixes** — priority order, Blocking items first

> Individual skills can also be run directly: `/aem-security`, `/aem-performance`, `/aem-cloudmanager`, `/aem-sonar`
>
> **Additional targeted skills** for specific areas — invoke directly when needed:
> - `/aem-oak-index` — Oak index type, coverage, and async configuration
> - `/aem-headless` — Content Fragment models, GraphQL persisted queries, CF Java integration
