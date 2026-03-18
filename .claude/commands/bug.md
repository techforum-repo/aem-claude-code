---
description: Investigate an AEM bug — trace the cause across Sling Models, OSGi services, HTL, and content
allowed-tools: Read, Grep, Glob, Bash(git log *), Bash(git log --oneline *)
argument-hint: "[bug description or Jira/GitHub/Bitbucket issue reference — include what was expected, what happened, which environment]"
---

Investigate: $ARGUMENTS

## Step 1 — Fetch issue context if a reference is provided

**If a Jira ticket reference is provided** (e.g. `PROJ-456`):
- Use the Jira MCP to fetch the ticket summary, description, steps to reproduce, and any comments
- Use this as the primary source of truth for the bug details

**If a GitHub issue URL or number is provided**:
- Use the GitHub MCP to fetch the issue title, description, reproduction steps, and comments

**If a Bitbucket issue URL is provided**:
- Use the Bitbucket MCP to fetch the issue details and comments

**If only a freeform description is provided**:
- Use that description as the basis for investigation

## Step 2 — Investigate

Start by reading files identified from the bug description. Run `git log --oneline -20` to check recent changes that may be related.

1. Identify the affected component, service, or content path from the description
2. Trace the request path — Sling resolution → resource type → Sling Model → service → HTL
3. Check for recent changes to the affected area via `git log`
4. Look for common AEM failure patterns:
   - Null resource or missing `sling:resourceType`
   - `ResourceResolver` closed before use
   - Query returning no results — missing index or wrong path
   - OSGi service not bound (null reference at runtime)
   - HTL expression with wrong or missing output context
   - Content package filter missing a required path
   - OSGi config in wrong runmode folder or wrong PID filename
5. Propose a fix once the root cause is identified
6. Suggest how to verify the fix and prevent recurrence

## Output

1. Root cause analysis
2. Supporting evidence — file, line, log snippet
3. Proposed fix
4. Verification steps
