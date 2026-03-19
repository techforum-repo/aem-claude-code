#!/usr/bin/env python3
"""
PostCompact hook: after context compaction, print a brief AEM rules reminder
so Claude retains the most critical project conventions in the new context window.
"""
import sys

REMINDER = """
=== AEM PROJECT CONTEXT (post-compaction reminder) ===
- Never use admin ResourceResolver or loginAdministrative — use service users
- Always close ResourceResolver and Session with try-with-resources
- Keep business logic in Sling Models / OSGi services, not in HTL
- JCR queries must be indexed, bounded, and never run inside loops
- Place OSGi config in ui.config; keep ui.apps immutable
- Use SLF4J parameterized logging only
- Never call Thread.sleep() in servlets, jobs, schedulers, or workflow steps
- For large child node iteration use JCR Node API (node.getNodes()) not Sling API (resource.listChildren())
- Protect against XSS: use XSSAPI methods (encodeForHTML, encodeForHTMLAttr, encodeForJSString, filterHTML) — never manual string escaping
=======================================================
"""

print(REMINDER)
sys.exit(0)
