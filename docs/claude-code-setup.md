# Claude Code setup guide

This guide explains how to set up Claude Code for this AEM repository, covering installation, configuration, IDE integration, and tips for effective use.

## Installation

### macOS / Linux

```bash
npm install -g @anthropic-ai/claude-code
```

### Windows

**Option 1 — WinGet (recommended):**
```powershell
winget install Anthropic.ClaudeCode
```

**Option 2 — PowerShell installer:**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**Option 3 — npm (requires Node.js):**
```powershell
npm install -g @anthropic-ai/claude-code
```

> **Windows requirement:** Claude Code requires [Git for Windows](https://git-scm.com/downloads/win) to run shell commands. If Git Bash is not detected automatically, add this to `.claude/settings.json`:
> ```json
> { "env": { "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe" } }
> ```

**Option 4 — WSL (Windows Subsystem for Linux):**
Run Claude Code inside WSL for full Linux compatibility. WSL 2 is recommended (supports sandboxing). Follow the Linux installation steps inside your WSL terminal.

### Verify installation

```bash
claude --version
```

## Starting Claude Code

Always start from the repository root so Claude can inspect the full worktree.

**VS Code extension:** Open your AEM project folder — Claude Code loads automatically.

**CLI (all platforms):**
```bash
cd /path/to/your-aem-project
claude
```

On Windows, run this from PowerShell, CMD, Git Bash, or WSL. The VS Code extension handles this automatically if you use that instead.

Claude Code will automatically load:
- `CLAUDE.md` — global repository guidance
- `.claude/rules/*.md` — scoped rules that activate when you work on matching files
- `.claude/settings.json` — permission rules

## Configuration files in this repository

### `CLAUDE.md`
Loaded on every session. Contains module structure, build commands, and core AEM rules. Edit this to match your project's actual Maven profiles, AEM host/port, and conventions.

Keep `CLAUDE.md` under 200 lines — files longer than this consume more context and reduce rule adherence. If your project needs more guidance, split content into `.claude/rules/` files and reference them with the `@` import syntax:

```
# CLAUDE.md
@.claude/rules/core-java.md
@.claude/rules/ui-apps.md
```

### `.claude/rules/`
Scoped rule files applied automatically when Claude reads or edits matching files. No action needed — they activate based on `paths:` frontmatter patterns in each file.

### `.claude/commands/`
Custom slash commands for repeatable tasks. Invoke them with `/project:` followed by the command name.

> **Commands vs Skills:** This repository uses both intentionally. Commands live in `.claude/commands/project/` and are invoked as `/project:<name>` — the subdirectory gives them a namespace that avoids conflicts with Claude Code built-ins. Skills live in `.claude/skills/` and are invoked as `/<name>` — they support `model:` overrides and `user-invocable: false` which commands do not. Commands orchestrate; skills do focused domain checks.

### `.claude/agent-memory/`

Agents with `memory: project` accumulate codebase knowledge across sessions and store it here. Two agents use this:

- **`aem-inspector`** — learns your component patterns, data flows, and risks over time
- **`aem-refactor`** — remembers naming conventions and structural decisions already applied

**Commit this folder to share memory across the team** — one developer's deep component analysis benefits everyone. Add to your repository and commit:

```bash
git add .claude/agent-memory/
git commit -m "Add accumulated agent memory"
```

If you prefer per-developer memory (each developer builds their own), add to `.gitignore`:

```gitignore
.claude/agent-memory/
```

### `.claude/hooks/`
Shell scripts that run automatically at lifecycle events. This repository includes one hook:

- **`guard-sensitive-files.py`** (`PreToolUse`) — blocks Claude from editing files matching credential patterns (`.env`, `*secret*`, `*keystore*`, etc.). Written in Python for cross-platform compatibility (Windows, Linux, macOS). Exit code 2 stops the action and shows a message.

To add your own hooks, register them in `.claude/settings.json` under `"hooks"`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/my-guard.py" }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [{ "type": "command", "command": "python3 .claude/hooks/post-format.py" }]
      }
    ]
  }
}
```

Common AEM hook use cases:
- `PreToolUse` / `Write|Edit` — block editing credential or environment files
- `PostToolUse` / `Write|Edit` on `*.java` — auto-run `mvn spotless:apply` to keep formatting
- `PostToolUse` / `Write|Edit` on `*.html` — validate HTL syntax

### `.claude/settings.json`
Controls which shell commands Claude can run automatically vs. which require approval. This file is committed to the repository and shared with the team.

For personal overrides (e.g. allowing additional commands on your machine), use `.claude/settings.local.json` — this file is git-ignored and not shared.

## Available commands

Five commands cover all common AEM development tasks. Skills can be chained by commands or invoked directly.

**Commands** — invoked as `/project:command-name`:

| Command | Use when |
|---|---|
| `/project:review` | Code review before committing or opening a PR — spawns parallel reviewer agents, merges findings |
| `/project:create` | Creating any AEM artifact — describe what you need, Claude detects the type |
| `/project:explain` | Understanding a component, or assessing Cloud Manager pipeline impact |
| `/project:pr` | Generating a PR description from the current branch diff |
| `/project:bug` | Investigating a bug by tracing the AEM request path |

**Skills** — invoked directly by name for targeted, standalone checks:

| Skill | Use when |
|---|---|
| `/aem-security` | Quick security check on a specific file or class |
| `/aem-performance` | Quick performance check — queries, resolvers, PostConstruct |
| `/aem-cloudmanager` | Check packaging and OakPAL risks before merging |
| `/aem-sonar` | Check SonarCloud quality before opening a PR |

## IDE integration

### VS Code

**Option 1 — VS Code extension (recommended):**

Install the official Claude Code extension from the VS Code Marketplace (search `Claude Code` by Anthropic, or use the extension ID `anthropic.claude-code`). Requires VS Code 1.98.0 or higher.

The extension provides:
- Native panel UI inside VS Code (not just a terminal)
- Interactive diff viewing and plan review before accepting changes
- File references with `@` mentions and line ranges
- Multiple conversation tabs

After installing the extension, open your AEM project folder in VS Code — Claude Code loads `CLAUDE.md`, rules, and settings automatically.

**Option 2 — Integrated terminal:**

1. Open the integrated terminal (`Ctrl+\``)
2. Navigate to your AEM project root
3. Run `claude`

To make hidden files visible in the VS Code Explorer so `.claude/` appears:

```json
// .vscode/settings.json
{
  "files.exclude": {
    "**/.claude": false
  }
}
```

Recommended extensions for AEM development:
- Extension Pack for Java (Microsoft)
- Maven for Java (Microsoft)
- SonarLint (SonarSource)
- XML (Red Hat)

## MCP servers (team-shared)

`.mcp.json` at the repository root is loaded automatically for all team members. Configure it to match your source control and issue tracker. The `/project:pr` and `/project:bug` commands use whichever MCP is available — pass a ticket or issue reference as an argument to pull full context automatically.

### GitHub

```json
{
  "mcpServers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

Set `GITHUB_TOKEN` in your environment before starting Claude Code.

### Bitbucket

```json
{
  "mcpServers": {
    "bitbucket": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-bitbucket"],
      "env": {
        "BITBUCKET_USERNAME": "${BITBUCKET_USERNAME}",
        "BITBUCKET_APP_PASSWORD": "${BITBUCKET_APP_PASSWORD}"
      }
    }
  }
}
```

Generate a Bitbucket App Password under **Account settings → App passwords** with repository read scope.

### Jira

```json
{
  "mcpServers": {
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
  }
}
```

Generate a Jira API token under **Atlassian account → Security → API tokens**.

With Jira configured:
```
/project:pr PROJ-123
```
Claude fetches the ticket requirements and aligns the PR summary with the acceptance criteria.

```
/project:bug PROJ-456
```
Claude fetches the bug report, reproduction steps, and comments before starting the investigation.

### Combining source control and Jira

You can include both in `.mcp.json` — Claude uses whichever tool is relevant:

```json
{
  "mcpServers": {
    "github": { ... },
    "jira": { ... }
  }
}
```

Add a personal-only MCP server (not committed to git):
```bash
claude mcp add --scope local my-server -- npx -y some-mcp-package
```

## Permissions

`.claude/settings.json` uses a three-tier permission model evaluated in order: **deny → ask → allow**.

| Tier | Behaviour |
|---|---|
| `allow` | Claude runs the command without prompting |
| `ask` | Claude prompts you before running — you approve or deny each time |
| `deny` | Claude cannot run the command at all |
| *(unlisted)* | Defaults to asking for approval |

The defaults in this repository:

- **Allowed automatically**: `mvn` builds, `git log`, `git diff`, `git status`, `git show`, `git branch`, `npm`
- **Ask before running**: `git commit`, `git checkout`, `git switch`, `git reset`, `git stash`
- **Always blocked**: `rm -rf`, credentials in curl commands, `mvn deploy`, `git push --force`

**Wildcard syntax**: a space before `*` matters.
- `Bash(git log *)` — matches `git log --oneline`, `git log -10`, but NOT `git logbook`
- `Bash(git log*)` — matches both `git log --oneline` AND `git logbook`

Use space-delimited wildcards for precise matching. Example configuration:

```json
{
  "permissions": {
    "allow": [
      "Bash(mvn *)",
      "Bash(mvn clean*)",
      "Bash(git log *)",
      "Bash(git diff *)",
      "Bash(npm *)"
    ],
    "ask": [
      "Bash(git commit *)",
      "Bash(git checkout *)"
    ],
    "deny": [
      "Bash(rm -rf*)",
      "Bash(git push --force*)"
    ]
  }
}
```

For personal additions that should not be committed, use `.claude/settings.local.json` — it has the same structure and is automatically git-ignored.

## Useful Claude Code features for AEM development

### Reading multiple files at once
Claude can read several files in parallel. List them explicitly:

```
Read these files and explain how they work together:
- core/src/main/java/com/example/models/ProductModel.java
- ui.apps/src/main/content/jcr_root/apps/myproject/components/product-card/product-card.html
- ui.apps/src/main/content/jcr_root/apps/myproject/components/product-card/_cq_dialog/.content.xml
```

### Running Maven builds
Ask Claude to build and interpret the output:

```
Run mvn clean install and fix any compilation errors.
```

```
Run mvn test on the core module and explain any failures.
```

### Git diff in context
For any review or PR task, Claude runs `git diff` automatically. You can also ask directly:

```
Show me what changed in the last 3 commits and summarize the risk.
```

### Checking CRXDE or AEM state
Claude cannot connect to a running AEM instance directly, but it can generate curl commands you can run:

```
Generate a curl command to check the bundle state of com.example.core via the Felix console.
```

## Recommended daily workflow

1. Start Claude Code from the repository root: `claude` (or open the VS Code extension)
2. For new feature work: `/project:create` — describe what you need, Claude detects the artifact type
3. Before committing: `/project:review` — spawns security, performance, Cloud Manager, and SonarCloud reviewer agents in parallel, merges findings
4. For a quick focused check: `/aem-cloudmanager` or `/aem-security` on specific files
5. Before opening a PR: `/project:pr` for the summary, `/project:explain` for pipeline impact
6. For bugs: `/project:bug` with a description of what is wrong and on which environment

## Troubleshooting

**Claude does not see my file changes**
Make sure you are running Claude Code from the repository root. Claude reads files directly from disk, so saved changes are always visible.

**A command is blocked by settings.json**
Check the `deny` list in `.claude/settings.json`. If the command is safe for your workflow, add it to the `allow` list. For personal additions that should not be shared with the team, use `.claude/settings.local.json` instead — it is automatically git-ignored.

**Rules do not seem to apply**
Confirm the file path matches the `paths:` pattern in the rule file. Claude Code applies rules when a file matching the pattern is read or edited in the session.

**Build errors after Claude's changes**
Ask Claude to fix them directly:
```
Run mvn clean compile and fix any errors.
```
