---
description: Draft a pull request summary with modules changed, risks, and test plan
allowed-tools: Read, Bash(git diff *), Bash(git diff), Bash(git log *), Bash(git status)
argument-hint: "[base branch or issue/ticket reference — e.g. 'main', 'PROJ-123', 'github.com/org/repo/issues/42']"
---

Draft a pull request summary for the current changes.

$ARGUMENTS

## Step 1 — Gather change context

Run `git diff main...HEAD` and `git log main...HEAD --oneline` to gather the diff and commit history.

**If a Jira ticket reference is provided** (e.g. `PROJ-123`):
- Use the Jira MCP to fetch the ticket summary, description, and acceptance criteria
- Align the PR summary with the ticket's stated requirements and definition of done

**If a GitHub issue URL or number is provided** (e.g. `#42` or a full GitHub URL):
- Use the GitHub MCP to fetch the issue title, description, and any linked requirements
- Align the PR summary with the issue's stated requirements

**If a Bitbucket issue URL is provided**:
- Use the Bitbucket MCP to fetch the issue details
- Align the PR summary with the issue's stated requirements

**If no issue or ticket reference is provided**:
- Base the summary entirely on what is found in the git diff and commit history

## Step 2 — Draft the PR summary

Base the summary on confirmed diff findings. Do not invent implementation details.

- Identify the business or technical purpose of the change set
- Group changes by module or functional area
- Call out testing performed, missing validation, or recommended checks
- Mention risks, rollback considerations, and any AEM, SonarCloud, or Cloud Manager notes
- If the change is documentation or tooling only, say so clearly
- Separate confirmed details (from diff) from assumptions

## Output

## Summary
<1-3 bullet points>

## Modules changed
<grouped by module>

## Risks & notes
<Cloud Manager, OakPAL, Dispatcher, SonarCloud>

## Test plan
<what was tested and what still needs validation>
