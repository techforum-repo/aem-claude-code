# AEM Claude Code Guidance

Reusable Claude Code configuration for an enterprise Adobe Experience Manager as a Cloud Service (AEMaaCS) project. Works on **Windows, Linux, and macOS** via the VS Code extension or CLI.

---

## Quick start

1. Copy `CLAUDE.md` into the root of your AEM repository.
2. Copy the `.claude/` folder into the root of your AEM repository.
3. Adjust module names, build commands, and runmode names in `CLAUDE.md` to match your project.
4. Verify `.claude/settings.json` permission rules match your team's workflow.
5. Add `.claude/settings.local.json` to your `.gitignore` for personal permission overrides that should not be committed.

---

## Repository structure

### `CLAUDE.md`
Loaded automatically on every session. Defines module boundaries, AEMaaCS conventions, Cloud Manager safety rules, and build commands.

---

### `.claude/rules/`
Scoped instruction files applied automatically when Claude reads or edits files matching the `paths:` pattern. Multiple rules can apply to the same file — Claude Code merges them, applying the strictest guidance when they overlap.

| File | Paths |
|---|---|
| `core-java.md` | `core/src/main/**/*.java` |
| `core-java-security.md` | `core/src/main/**/*.java` |
| `core-java-performance.md` | `core/src/main/**/*.java` |
| `core-java-tests.md` | `core/src/test/**/*.java` |
| `ui-apps.md` | `ui.apps/**/*.{html,xml,js,css,scss}` |
| `ui-apps-structure.md` | `ui.apps.structure/**/*.xml` |
| `ui-content.md` | `ui.content/**/*.xml` |
| `ui-config.md` | `ui.config/**/*.xml` |
| `all-module.md` | `all/**/*.xml` |
| `frontend-base.md` | `ui.frontend/**/*.{js,ts,css,scss}` |
| `frontend-react.md` | `ui.frontend.react/**/*.{js,ts,css,scss}` |
| `frontend-spa.md` | `ui.frontend.spa/**/*.{js,ts,css,scss}` |
| `devops.md` | `devops/**/*` |
| `dispatcher.md` | `devops/**/*.{conf,any,vhost,farm}` |
| `hooks.md` | `hooks/**/*` |
| `oak-index.md` | `ui.apps/**/oak:index/**/*.xml` |
| `content-fragments.md` | `ui.content/**/settings/dam/cfm/**/*.xml`, CF-related Java classes |
| `caconfig.md` | `ui.content/**/sling:configs/**/*.xml`, CAConfig Java interfaces |
| `i18n.md` | `ui.apps/**/i18n/**/*.json`, `ui.apps/**/i18n/**/*.xml` |

---

### `.claude/commands/`
Five slim entry-point commands. Each routes to the right agents, skills, or creation rules automatically.

| Command | What it does |
|---|---|
| `/project:review` | Full AEM review — spawns security, performance, Cloud Manager, and SonarCloud reviewer agents in parallel, then consolidates findings |
| `/project:create` | Smart creation — detects artifact type from your description and applies the right rules |
| `/project:explain` | Explains a component end-to-end, or analyses Cloud Manager pipeline impact of current changes |
| `/project:pr` | Drafts a PR summary with modules changed, risks, and test plan |
| `/project:bug` | Investigates a bug by tracing the AEM request path |

#### How to invoke

```
/project:review
```
*(runs `git diff`, spawns four reviewer agents in parallel, merges all findings into one report)*

```
/project:review core/src/main/java/com/example/models/ProductModel.java
```

```
/project:create
A product card component with title, image, price, and CTA. Style system variants for dark/light backgrounds.
```

```
/project:create
Sling Model for the product card at apps/myproject/components/product-card
```

```
/project:explain ui.apps/src/main/content/jcr_root/apps/myproject/components/product-card
```

```
/project:bug
The product card shows a blank title on publish but works on author.
```

### `.claude/skills/`
Focused, reusable skills. Invocable directly by name for quick targeted checks. `/project:review` uses dedicated reviewer agents instead — skills are the lightweight option when you only need one domain checked.

| Skill | Direct invocation | What it checks |
|---|---|---|
| `aem-security` | `/aem-security` | Admin resolver, query injection, path validation, hardcoded secrets |
| `aem-performance` | `/aem-performance` | Unbounded queries, query-in-loop, `@PostConstruct` overhead, long-lived resolvers |
| `aem-cloudmanager` | `/aem-cloudmanager` | OakPAL violations, embed order, Dispatcher SDK, deployment safety |
| `aem-sonar` | `/aem-sonar` | Complexity, duplication, resource leaks, SonarCloud security hotspots. Uses `model: haiku`. |
| `aem-oak-index` | `/aem-oak-index` | Oak index type, property coverage, `evaluatePathRestrictions`, async config, index creation |
| `aem-headless` | `/aem-headless` | CF model backward compatibility, GraphQL persisted queries, CF Java integration, CORS, Dispatcher rules |
| `aem-project-conventions` | *(not user-invocable — auto-applied)* | Always-loaded team conventions: package naming, Sling Model patterns, HTL conventions, OSGi config placement, test structure |

Run a single skill for a quick focused check before committing:

```
/aem-cloudmanager
```
*(checks current diff for OakPAL and deployment risks only)*

---

### `.claude/agents/`
Custom subagents with their own isolated context window, tool allowlist, and model. Claude delegates to them automatically based on the `description:` field.

| Agent | When Claude uses it |
|---|---|
| `aem-inspector` | Whenever `/project:explain` is called with a component path or class name. Uses `model: opusplan` (Opus for planning, Sonnet for execution) and `memory: project` to accumulate component knowledge across sessions. |
| `aem-refactor` | When asked to refactor, rename, or restructure AEM code. Runs in an isolated git worktree (`isolation: worktree`) — your branch is unchanged until you merge. |
| `aem-security-reviewer` | Spawned in parallel by `/project:review` — security domain (admin resolver, query injection, path validation, hardcoded secrets). |
| `aem-performance-reviewer` | Spawned in parallel by `/project:review` — performance domain (JCR queries, traversal, resolver lifecycle, threading). |
| `aem-cloudmanager-reviewer` | Spawned in parallel by `/project:review` — Cloud Manager domain (OakPAL, embed order, Dispatcher SDK, deployment safety). |
| `aem-sonar-reviewer` | Spawned in parallel by `/project:review` — code quality domain (complexity, duplication, resource leaks). Uses `model: haiku`. |

Agents differ from skills: a skill runs inline in your conversation; an agent gets a fresh isolated context, runs to completion, and returns a summary. Use agents for deep multi-file analysis tasks that would otherwise pollute the main conversation with file contents.

### `.claude/hooks/`
Shell scripts executed at Claude Code lifecycle events. Registered in `settings.json` under `"hooks"`.

Included hooks:
- **`guard-sensitive-files.py`** (`PreToolUse`) — blocks Claude from editing files matching credential patterns (`.env`, `*secret*`, `*keystore*`). Written in Python for cross-platform compatibility. Add patterns to `SENSITIVE_PATTERNS` to match your project's naming conventions.
- **`post-compact.py`** (`PostCompact`) — after context compaction in long sessions, prints a brief AEM rules reminder so Claude retains the most critical project conventions in the new context window.

Supported events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `SessionStart`, `Stop`, and others. See `docs/claude-code-setup.md` for examples.

### `.claude/settings.json`
Permission rules that control which shell commands Claude Code can run automatically vs. which require approval. Uses a three-tier model: `allow` / `ask` / `deny`.

Adjust the lists to match your team's conventions. The defaults allow common Maven and git read commands, prompt for git write operations, and block destructive or credential-exposing operations.

> **Skills:** `.claude/skills/` is the newer equivalent of `.claude/commands/` with additional frontmatter options (`context: fork`, `agent:`, supporting files). Both work for slash-command invocation. Migrate to `.claude/skills/` when you need subagent isolation or multi-file skill structure.

---

### `docs/`

| File | Description |
|---|---|
| `docs/claude-code-cheatsheet.md` | Full cheatsheet of freeform and command-based requests by category |
| `docs/claude-code-setup.md` | Setup guide — installation, IDE integration, permissions, MCP, daily workflow |

---

## Recommended usage model

1. Keep broad standards in `CLAUDE.md`
2. Keep module-specific, path-scoped guidance in `.claude/rules/`
3. Keep entry-point commands slim in `.claude/commands/` — route and orchestrate, don't duplicate rule content
4. Keep focused, reusable logic in `.claude/skills/` — individual skills can be chained by commands or invoked directly
5. Adjust `settings.json` to reflect your team's trust boundaries

---

## MCP servers

`.mcp.json` at the repository root is loaded automatically for all team members. Configure it to match your team's source control and issue tracker.

`/project:pr` and `/project:bug` use whichever MCP is configured — pass a Jira ticket, GitHub issue, or Bitbucket issue reference as an argument and Claude fetches the full context automatically. Without a reference, both commands fall back to git only.

### Source control — pick one

**GitHub** (default in `.mcp.json`):
```json
"github": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
}
```

**Bitbucket:**
```json
"bitbucket": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-bitbucket"],
  "env": {
    "BITBUCKET_USERNAME": "${BITBUCKET_USERNAME}",
    "BITBUCKET_APP_PASSWORD": "${BITBUCKET_APP_PASSWORD}"
  }
}
```

### Issue tracker — Jira (recommended for AEM enterprise teams)

```json
"jira": {
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "mcp-atlassian"],
  "env": {
    "JIRA_URL": "${JIRA_URL}",
    "JIRA_USERNAME": "${JIRA_USERNAME}",
    "JIRA_API_TOKEN": "${JIRA_API_TOKEN}"
  }
}
```

With Jira configured, `/project:pr PROJ-123` fetches the ticket requirements and aligns the PR summary with the acceptance criteria. `/project:bug PROJ-456` fetches reproduction steps and comments before starting the investigation.

### Other useful MCP servers

| Server | Use case |
|---|---|
| Fetch | Pull live AEM Javadocs, Sling API docs, or external specs into context |
| Custom AEM MCP | Query CRXDE, Felix console, or AEM APIs directly |

Add personal-only MCP servers (with credentials) using local scope — not committed to git:
```bash
claude mcp add --scope local my-server -- npx -y some-mcp-package
```

---

## Implemented Claude Code features

| Feature | Where used |
|---|---|
| **`model: opusplan`** | `aem-inspector` agent — Opus reasons about cross-module structure, Sonnet executes the analysis |
| **`model: haiku`** | `aem-sonar` skill — mechanical checklist checks don't need a heavyweight model |
| **`model: sonnet`** | `aem-refactor` agent — balanced model for reading, writing, and reasoning about code changes |
| **`isolation: worktree`** | `aem-refactor` agent — refactoring runs in an isolated git copy, branch is safe until merged |
| **`memory: project`** | `aem-inspector` agent — accumulates component knowledge across sessions in `.claude/agent-memory/` |
| **`user-invocable: false`** | `aem-project-conventions` skill — always-loaded team conventions applied silently on every task |
| **`context: fork`** | `review.md` command — runs in a forked context so the full review doesn't pollute the main conversation |
| **Agent teams** | `review.md` spawns 4 reviewer agents in parallel (security, performance, Cloud Manager, SonarCloud), each with its own isolated context, then merges findings |
| **`/batch`** | Documented in cheatsheet — bulk convention fixes, null-check additions, log statement migrations |
| **`/loop`** | Documented in cheatsheet — Cloud Manager pipeline polling, test failure watching |
| **Plan mode** | Documented in cheatsheet — read-only exploration before large refactors or filter changes |

---

## Extending this repository

### Add a scoped rule
Create `.claude/rules/<topic>.md` with `paths:` frontmatter. Claude applies it automatically when matching files are read or edited. No registration needed.

```markdown
---
description: Rules for custom base components
paths:
  - "ui.apps/**/components/base/**/*.html"
  - "ui.apps/**/components/base/**/*.xml"
---
# Base component rules
...
```

### Add a custom agent
Create `.claude/agents/<agent-name>.md`. Claude delegates to it automatically when the task matches the `description:` field. Use agents for deep multi-file tasks that would otherwise flood the main context.

```markdown
---
name: aem-accessibility-auditor
description: Use when asked to audit AEM components for WCAG 2.1 accessibility compliance
tools: Read, Grep, Glob
model: sonnet
---

Audit the component at $ARGUMENTS for accessibility:
- HTL aria attributes and landmark roles
- Dialog field labels and descriptions
- Color contrast in component styles
- Keyboard navigation support
```

### Add a new skill
Create `.claude/skills/<skill-name>/SKILL.md`. The skill is immediately invocable as `/<skill-name>` for targeted checks. To include it in full reviews, also create a corresponding reviewer agent in `.claude/agents/` and reference it in `review.md`.

```markdown
---
name: aem-accessibility
description: AEM accessibility review — WCAG 2.1, HTL aria attributes, dialog labels
allowed-tools: Read, Grep, Glob
argument-hint: "[file or component path]"
---
Review `$ARGUMENTS` for accessibility issues...
```

### Extend the /create command
Add a row to the routing table in `create.md` to handle new artifact types.

### Add a hook
Write a Python script in `.claude/hooks/`. Register it in `.claude/settings.json`:

```json
"PostToolUse": [
  {
    "matcher": "Write|Edit",
    "hooks": [{ "type": "command", "command": "python3 .claude/hooks/my-hook.py || python .claude/hooks/my-hook.py" }]
  }
]
```

### Add MCP servers (team-shared)
Create `.mcp.json` at the repository root. All team members pick it up automatically.

```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"]
    }
  }
}
```

### Future skill patterns (not yet implemented, ready to add)
- **`aem-accessibility/SKILL.md`** — WCAG 2.1 HTL review
- **`aem-multisite/SKILL.md`** — Multi-site Manager and inheritance chain rules

---

## Suggested next steps

- Refine commands based on real team usage patterns
- Add project-specific rules for custom base components or internal utility libraries
- Expand `settings.json` with additional safe Maven profiles for your project
- Add `.mcp.json` at the repo root for team-shared MCP servers (GitHub, Jira, Slack, etc.)
