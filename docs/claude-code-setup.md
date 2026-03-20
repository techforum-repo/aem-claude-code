# Claude Code setup guide

This guide covers installation and daily use. For full configuration reference (rules, hooks, permissions, MCP, agents), see the [README](../README.md).

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

**Option 3 — npm:**
```powershell
npm install -g @anthropic-ai/claude-code
```

> **Windows requirement:** Claude Code requires [Git for Windows](https://git-scm.com/downloads/win). If Git Bash is not detected automatically, add to `.claude/settings.json`: `{ "env": { "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe" } }`

### Verify

```bash
claude --version
```

## Starting Claude Code

Always start from the repository root so Claude can inspect the full worktree.

**VS Code extension:** Open your AEM project folder — Claude Code loads automatically.

**CLI:**
```bash
cd /path/to/your-aem-project
claude
```

Claude Code automatically loads `CLAUDE.md`, `.claude/rules/*.md`, and `.claude/settings.json` on start.

## Commands and skills

**Commands** — invoke as `/project:<name>`:

| Command | Use when |
|---|---|
| `/project:review` | Code review before committing — spawns six parallel reviewer agents |
| `/project:create` | Creating any AEM artifact — describe what you need |
| `/project:explain` | Understanding a component or assessing Cloud Manager pipeline impact |
| `/project:pr` | Generating a PR description from the current branch diff |
| `/project:bug` | Investigating a bug by tracing the AEM request path |

**Skills** — invoke directly:

| Skill | Use when |
|---|---|
| `/aem-security` | Quick security check on a specific file or class |
| `/aem-performance` | Quick performance check — queries, resolvers, PostConstruct |
| `/aem-cloudmanager` | Check packaging and OakPAL risks before merging |
| `/aem-sonar` | Check SonarCloud quality before opening a PR |
| `/aem-oak-index` | Review or create Oak indexes |
| `/aem-headless` | Review CF models, GraphQL queries, CORS, and Dispatcher rules |

## Daily workflow

1. Start from the repository root: `claude` (or open the VS Code extension)
2. New feature: `/project:create` — describe what you need
3. Before committing: `/project:review` — six reviewer agents in parallel
4. Quick focused check: `/aem-security` or `/aem-cloudmanager` on specific files
5. Before opening a PR: `/project:pr` for the summary
6. For bugs: `/project:bug` with a description of the issue

## IDE integration

Install the Claude Code extension from the VS Code Marketplace (`anthropic.claude-code`, requires VS Code 1.98.0+). The extension provides a native panel UI, interactive diff viewing, and multiple conversation tabs.

To make `.claude/` visible in the VS Code Explorer:

```json
// .vscode/settings.json
{ "files.exclude": { "**/.claude": false } }
```

## Troubleshooting

**Claude does not see my file changes** — Run Claude Code from the repository root. Claude reads files directly from disk.

**A command is blocked** — Check the `deny` list in `.claude/settings.json`. For personal additions that should not be shared, use `.claude/settings.local.json` (git-ignored).

**Rules do not apply** — Confirm the file path matches the `paths:` pattern in the rule file.

**Build errors after Claude's changes** — Ask Claude to fix them: `Run mvn clean compile and fix any errors.`
