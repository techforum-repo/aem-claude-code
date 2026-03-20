---
description: Comprehensive AEM code review — spawns a six-teammate agent team (security, performance, Cloud Manager, SonarCloud, maintainability, accessibility) in parallel, then consolidates all findings into one report
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git diff), Bash(git status), Bash(git log *), TeamCreate, SendMessage
argument-hint: "[file or class path, or leave blank to review current branch diff]"
disable-model-invocation: true
---

Review target: $ARGUMENTS

If no path is provided, run `git diff` to identify what changed in the current branch. Use that diff as the review target.

## Step 1 — Create a native agent team

**Use the agent teams feature** to create a team with exactly five teammates. Do not use subagents or the Agent tool — use `TeamCreate` to spawn real teammates that share a task list and can message each other directly.

Create the team with these six teammates:

**teammate: security-reviewer**
Prompt: Review $ARGUMENTS for AEM security issues. Focus on: admin resolver usage, query injection from user input, unvalidated path input, hardcoded secrets, servlet exposure, missing XSSAPI output encoding. Report every finding as Blocking / Warning / Suggestion with file and line reference.

**teammate: performance-reviewer**
Prompt: Review $ARGUMENTS for AEM performance issues. Focus on: JCR queries (indexed, bounded, no loops), JCR Node API vs Sling API for large child iteration, ResourceResolver/Session lifecycle (must use try-with-resources), @PostConstruct overhead, Thread.sleep in request paths. Report every finding as Blocking / Warning / Suggestion with file and line reference.

**teammate: cloudmanager-reviewer**
Prompt: Review $ARGUMENTS for AEM Cloud Manager and OakPAL issues. Focus on: ui.apps immutability, OSGi config in ui.config, package filter correctness, embed order in all/, Dispatcher SDK compatibility, Repoinit safety, deployment blockers. Report every finding as Blocking / Warning / Suggestion with file and line reference.

**teammate: sonar-reviewer**
Prompt: Review $ARGUMENTS for AEM code quality issues. Focus on: cyclomatic complexity, code duplication, null safety, unclosed resource leaks, SonarCloud security hotspots. Report every finding as Blocking / Warning / Suggestion with file and line reference.

**teammate: maintainability-reviewer**
Prompt: Review $ARGUMENTS for long-term maintainability. Focus on: (1) comment accuracy — are Javadoc and inline comments accurate and consistent with the actual code behaviour, or are they stale/misleading? (2) type design — are types well encapsulated with strong invariants, or do they expose unnecessary internals? (3) code simplification — is there unnecessary complexity or opportunities to simplify without changing behaviour? Report every finding as Blocking / Warning / Suggestion with file and line reference.

**teammate: accessibility-reviewer**
Prompt: Review $ARGUMENTS for accessibility issues. Focus on: missing or incorrect ARIA attributes (aria-label, aria-describedby, role), keyboard navigation and focus management, HTL output context for accessible markup, color contrast assumptions hardcoded in CSS/SCSS, missing alt text on images, form label associations, heading hierarchy, and WCM Core Component accessibility configuration. Report every finding as Blocking / Warning / Suggestion with file and line reference.

Teammates should message each other when a finding in one domain has implications for another (e.g. security finding that is also a performance risk).

## Step 2 — Inline checks (run in this context while teammates are working)

While teammates are running, perform these checks in the lead context:

- **Module placement** — are changes in the correct module? `ui.apps` immutable vs `ui.content`/`ui.config` mutable separation?
- **HTL** — correct output context on every expression, no business logic in HTL, backward-compatible dialog field changes
- **Resource lifecycle** — `ResourceResolver` and `Session` closed via try-with-resources in all code paths?
- **Tests** — meaningful assertions, null and edge-case coverage, no brittle mock-only tests?

## Step 3 — Wait for all teammates to finish, then consolidate

Once all six teammates have reported back, merge their findings with the inline checks into one report:

1. **Summary** — what was reviewed and scope
2. **All findings** — consolidated and deduplicated, labelled **Blocking** / **Warning** / **Suggestion**, grouped by domain (Security / Performance / Cloud Manager / Quality / Maintainability / Structure)
3. **Recommended fixes** — priority order, Blocking items first

Clean up the team after the report is delivered.

> Individual skills can also be run directly for a quick single-domain check: `/aem-security`, `/aem-performance`, `/aem-cloudmanager`, `/aem-sonar`
>
> **Additional targeted skills** for specific areas:
> - `/aem-oak-index` — Oak index type, coverage, and async configuration
> - `/aem-headless` — Content Fragment models, GraphQL persisted queries, CF Java integration
