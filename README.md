# AEM Claude Code Guidance

Reusable Claude Code configuration for an enterprise Adobe Experience Manager as a Cloud Service (AEMaaCS) project. Works on **Windows, Linux, and macOS** via the VS Code extension or CLI.

---

## Quick start

**Copy files into your AEM project root:**

```
CLAUDE.md  →  <project-root>/CLAUDE.md
.mcp.json  →  <project-root>/.mcp.json
.claude/   →  <project-root>/.claude/
```

**Then customise for your project:**

1. `CLAUDE.md` — update module names, Maven commands, AEM host/port, and package naming
2. `.claude/settings.json` — set `AEM_HOST`, ports, and any additional Maven profiles to allow
3. `.mcp.json` — swap GitHub for Bitbucket if needed; add Jira MCP if your team uses it
4. Add `.claude/settings.local.json` to `.gitignore` for personal permission overrides
5. Optionally commit `.claude/agent-memory/` to share accumulated agent knowledge across the team

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
| `integration-tests.md` | `it.tests/src/**/*.java`, `ui.tests/src/**/*.java`, `ui.tests/src/**/*.ts` |

---

### `.claude/commands/`
Five slim entry-point commands. Each routes to the right agents, skills, or creation rules automatically.

| Command | What it does |
|---|---|
| `/project:review` | Full AEM review — creates a native agent team with four specialist reviewer teammates (security, performance, Cloud Manager, SonarCloud), each in an isolated context, then consolidates findings |
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
| `aem-refactor` | When asked to refactor, rename, or restructure AEM code. Runs in an isolated git worktree (`isolation: worktree`) — your branch is unchanged until you merge. Uses `memory: project` to remember naming conventions and structural decisions across sessions. |
| `aem-security-reviewer` | Spawned in parallel by `/project:review` — security domain (admin resolver, query injection, path validation, hardcoded secrets). |
| `aem-performance-reviewer` | Spawned in parallel by `/project:review` — performance domain (JCR queries, traversal, resolver lifecycle, threading). |
| `aem-cloudmanager-reviewer` | Spawned in parallel by `/project:review` — Cloud Manager domain (OakPAL, embed order, Dispatcher SDK, deployment safety). |
| `aem-sonar-reviewer` | Spawned in parallel by `/project:review` — code quality domain (complexity, duplication, resource leaks). Uses `model: haiku`. |

Agents differ from skills: a skill runs inline in your conversation; an agent gets a fresh isolated context, runs to completion, and returns a summary. Use agents for deep multi-file analysis tasks that would otherwise pollute the main conversation with file contents.

### `.claude/hooks/`
Shell scripts executed at Claude Code lifecycle events. Registered in `settings.json` under `"hooks"`.

> **Prerequisite:** All hooks are Python scripts and require **Python 3** on PATH. Verify with `python3 --version`. Python 3 is pre-installed on macOS and most Linux distributions. On Windows, install from [python.org](https://www.python.org/downloads/) and ensure it is added to PATH during setup.

Included hooks:
- **`guard-sensitive-files.py`** (`PreToolUse`) — blocks Claude from editing files matching credential patterns (`.env`, `*secret*`, `*keystore*`). Written in Python for cross-platform compatibility. Add patterns to `SENSITIVE_PATTERNS` to match your project's naming conventions.
- **`post-format.py`** (`PostToolUse`) — after Claude writes or edits a Java file in `core/`, automatically runs `mvn spotless:apply -pl core` to keep formatting consistent. Requires the [Spotless Maven plugin](https://github.com/diffplug/spotless) in `core/pom.xml` (see below). If your team uses a different formatter, see [Using a different formatter](#using-a-different-formatter).

- **`post-dispatcher-validate.py`** (`PostToolUse`) — after Claude writes or edits a Dispatcher config file (`.any`, `.conf`, `.rules`, `.vars`, `.farm` under `conf.dispatcher.d/` or `conf.d/`), automatically runs the [AEM Dispatcher SDK validator](https://experienceleague.adobe.com/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools.html) to catch config errors immediately. Skips gracefully if the SDK validator is not installed.

  **Where to install the validator:**
  Download the Dispatcher Tools zip from the [AEM SDK](https://experience.adobe.com/#/downloads) and extract it. Either add the `bin/` directory to your PATH, or place the extracted folder at the standard fallback location:

  | Platform | Binary name | Fallback location |
  |---|---|---|
  | Linux / macOS | `validate` | `~/aem-sdk/dispatcher/bin/validate` |
  | Windows | `validator.exe` | `~/aem-sdk/dispatcher/bin/validator.exe` |

  Keep the SDK outside the project so it is not committed to source control. On Windows, ensure the path contains no spaces or special characters.

#### Setting up Spotless in `core/pom.xml`

Add the following inside `<build><plugins>` in your `core/pom.xml`:

```xml
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.43.0</version>
  <configuration>
    <java>
      <googleJavaFormat>
        <version>1.19.2</version>
        <!-- GOOGLE = 2-space indent  |  AOSP = 4-space indent (common in enterprise AEM) -->
        <style>GOOGLE</style>
      </googleJavaFormat>
    </java>
  </configuration>
  <executions>
    <execution>
      <goals><goal>check</goal></goals>
      <phase>verify</phase>
    </execution>
  </executions>
</plugin>
```

Verify it works before relying on the hook:

```bash
mvn spotless:apply -pl core
mvn spotless:check -pl core
```

The `check` goal is wired to the `verify` phase so Cloud Manager will fail the build if unformatted code is pushed.

#### Using a different formatter

Edit `.claude/hooks/post-format.py` and replace the command list in the `subprocess.run(...)` call:

| Formatter | Command list |
|---|---|
| Spotless (default) | `["mvn", "spotless:apply", "-pl", "core", "-q"]` |
| Eclipse formatter plugin | `["mvn", "formatter:format", "-pl", "core", "-q"]` |
| Checkstyle (check only, no auto-fix) | `["mvn", "checkstyle:check", "-pl", "core", "-q"]` |
| Palantir Java Format via Spotless | Change `<googleJavaFormat>` to `<palantirJavaFormat>` in `pom.xml`, keep same command |
| Custom shell script | `["bash", ".claude/hooks/format-java.sh", file_path]` |

**Spotless with Eclipse formatter plugin (`com.googlecode.maven-java-formatter-plugin`):**

```xml
<plugin>
  <groupId>com.googlecode.maven-java-formatter-plugin</groupId>
  <artifactId>maven-java-formatter-plugin</artifactId>
  <version>0.4</version>
  <configuration>
    <configFile>${project.basedir}/../eclipse-formatter.xml</configFile>
  </configuration>
</plugin>
```

```python
# post-format.py — replace the subprocess.run command list with:
["mvn", "formatter:format", "-pl", "core", "-q"]
```

If your project does not use any auto-formatter, remove the `PostToolUse` hook entry from `.claude/settings.json` — the other two hooks remain active independently.

- **`teammate-idle.py`** (`TeammateIdle`) — fires when a reviewer teammate is about to go idle. Checks if the teammate has produced a findings report (keywords: Blocking / Warning / Suggestion). If not, exits with code 2 to keep the teammate working until the report is complete.

- **`post-tool-failure.py`** (`PostToolUseFailure`) — logs tool failures with context (command, file path, error) to stderr. Helps diagnose recurring Maven build failures, Spotless errors, or blocked file edits without having to scroll back through the session.

- **`post-stop.py`** (`Stop`) — at the end of every session, prints a reminder to check `git status`, review the diff, and flush any non-obvious learnings to `.claude/agent-memory/` for team sharing.

- **`post-compact.py`** (`PostCompact`) — when a session grows long, Claude Code compresses the conversation history to free up context window space. After compaction, Claude loses the detailed rule context injected earlier in the session. This hook fires immediately after compaction and prints a short set of critical AEM rules back into context.

  The reminder is intentionally minimal — only rules where a single wrong edit causes a **production or security consequence** (admin resolver, resource leak, XSS, OakPAL failure, thread starvation). Style and convention rules are omitted to keep the reinjected context small. To customise, edit the `REMINDER` string in `post-compact.py`.

Supported events: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `SessionStart`, `Stop`, and others. See `docs/claude-code-setup.md` for examples.

### `.claude/settings.json`
Permission rules that control which shell commands Claude Code can run automatically vs. which require approval. Uses a three-tier model: `allow` / `ask` / `deny`.

Also sets project-wide environment variables (`AEM_HOST`, `AEM_PORT_AUTHOR`, `AEM_PORT_PUBLISH`) used in build commands. Override in `.claude/settings.local.json` for your local environment.

Adjust the lists to match your team's conventions. The defaults allow common Maven and git read commands, prompt for git write operations, and block destructive or credential-exposing operations.

> **Commands vs Skills:** Both are used in this repo and serve different purposes. **Commands** (`.claude/commands/project/`) are orchestration entry points invoked as `/project:<name>` (e.g. `/project:review`) — they coordinate agents and multi-step workflows. **Skills** (`.claude/skills/`) are focused, reusable domain tools invoked directly as `/<name>` (e.g. `/aem-security`) and support model overrides and auto-loading via `user-invocable: false`.

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

## LSP (Code intelligence)

`jdtls-lsp` and `typescript-lsp` are enabled in `settings.json` as project-scoped plugins. When the language server binaries are on PATH, Claude gains:

- **Real-time diagnostics** — type errors, missing imports, and syntax issues surfaced immediately after every edit
- **Go to definition** — navigate to Sling API, JCR, OSGi, and project class definitions directly
- **Find references** — trace usages of services, models, and interfaces across the codebase
- **Type information** — hover type info for `@Model`, `@Component`, `@Reference` annotations

### Install language server binaries

**Java (jdtls) — required for `core/` module:**

`jdtls` is not available via apt or brew — install it manually (same steps on Linux, macOS, and Windows):

**Linux / macOS:**
```bash
# 1. Create directories
mkdir -p ~/.local/share/jdtls ~/.cache/jdtls/workspace ~/.local/bin

# 2. Download latest milestone from Eclipse
curl -L -o /tmp/jdtls.tar.gz \
  "https://download.eclipse.org/jdtls/milestones/1.57.0/jdt-language-server-1.57.0-202602261110.tar.gz"

# 3. Extract
tar -xzf /tmp/jdtls.tar.gz -C ~/.local/share/jdtls

# 4. Symlink the launcher (ships with the package)
ln -sf ~/.local/share/jdtls/bin/jdtls ~/.local/bin/jdtls

# 5. Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH=$HOME/.local/bin:$PATH

# 6. Verify
which jdtls
```

**Windows:**
```powershell
# 1. Create directory
New-Item -ItemType Directory -Force "$env:LOCALAPPDATA\jdtls"

# 2. Download (update URL to latest milestone from https://download.eclipse.org/jdtls/milestones/)
Invoke-WebRequest -Uri "https://download.eclipse.org/jdtls/milestones/1.57.0/jdt-language-server-1.57.0-202602261110.tar.gz" `
  -OutFile "$env:TEMP\jdtls.tar.gz"

# 3. Extract (requires tar, available on Windows 10+)
tar -xzf "$env:TEMP\jdtls.tar.gz" -C "$env:LOCALAPPDATA\jdtls"

# 4. Add to PATH — add this to your PowerShell profile or System Environment Variables:
$env:PATH += ";$env:LOCALAPPDATA\jdtls\bin"
```

> jdtls ships with a `bin/jdtls` launcher script (Linux/macOS) and `bin/jdtls.bat` (Windows). No wrapper script needed — just add `bin/` to PATH.

> **First-run note:** jdtls indexes the Maven workspace on startup. This takes 3–5 minutes on first launch. CPU will drop to ~0% when indexing is complete. Until then LSP diagnostics will not fire.

**TypeScript — required for `ui.frontend*` modules:**

```bash
# Linux / macOS / Windows (via npm)
npm install -g typescript-language-server typescript
```

### Install the plugins

The plugins are pre-enabled in `settings.json`. On first session Claude Code will prompt you to install them, or install manually inside a Claude Code session:

```
/plugin install jdtls-lsp@claude-plugins-official
/plugin install typescript-lsp@claude-plugins-official
```

Restart the Claude Code session after installing — no `/reload-plugins` needed when starting fresh. Check `/plugin` → **Errors** tab if a language server binary is not found on PATH.

### Verify LSP is active

Ask Claude a question about a project-specific method:
```
What is the return type of ProductCardImpl.getCtaLink()?
```
- **LSP active** — Claude uses `lsp_hover` or `lsp_definition` tool calls
- **LSP not active** — Claude falls back to `Search` (grep)

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

---

## Future enhancements

Ideas and opportunities not yet implemented — ready to pick up:

### Skills
- **`aem-accessibility/SKILL.md`** — WCAG 2.1 HTL review against common AEM accessibility patterns
- **`aem-multisite/SKILL.md`** — Multi-site Manager, language copy, and Live Copy inheritance chain rules

### MCP servers
- **AEM MCP server (Adobe)** — Adobe is developing an official MCP server for AEM that would let Claude query the JCR, inspect content structures, and trigger replication directly from the conversation. Once available, this would replace the current `AEM_HOST`/`AEM_PORT` env var approach for live instance interactions.
- **Cloud Manager MCP server (Adobe)** — An official Cloud Manager MCP server would let Claude check pipeline status, read environment logs, and inspect deployment history without leaving the conversation. Pairs naturally with the `/project:pr` command and `/loop` polling pattern.

### Broader
- Refine commands based on real team usage patterns
- Add project-specific rules for custom base components or internal utility libraries
- Expand `settings.json` with additional safe Maven profiles for your project
