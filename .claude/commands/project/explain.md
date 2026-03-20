---
description: Explain an AEM component across all modules, or analyse the Cloud Manager pipeline impact of current changes
allowed-tools: Read, Grep, Glob, Bash(git diff *), Bash(git diff), Bash(git log *)
argument-hint: "[component path or class name, or leave blank for pipeline impact of current changes]"
disable-model-invocation: true
---

Explain: $ARGUMENTS

**If a component path or class name is provided** — delegate to the `aem-inspector` agent for a deep cross-module analysis:
- All related files across `core`, `ui.apps`, `ui.content`, `ui.config`, and frontend modules
- Complete data flow from authored content → Sling resolution → model → HTL → rendered output
- Authoring capabilities, dialog structure, and author-facing behavior
- OSGi service dependencies, service user mappings, and external integrations
- Known risks, null-safety gaps, and areas that commonly need attention when changing this component

**If no path is provided** — analyse the Cloud Manager pipeline impact of current changes:

Run `git diff main...HEAD` to identify what changed, then report:

- Which pipeline stages are affected (build, unit test, code quality, functional test, deployment)
- OakPAL concerns: overlapping filter roots, mutable content in `ui.apps`, embed order issues
- Deployment risks: content deletion from filter mode changes, service user or Repoinit failures
- Runtime impact: authoring, publish/Dispatcher, performance on high-traffic components
- Rollback risk: can this be reverted safely?
