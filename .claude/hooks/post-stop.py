#!/usr/bin/env python3
"""
Stop hook: at the end of every session, remind the developer to
commit any pending changes and prompt Claude to flush session memories.
"""
import sys

REMINDER = """
=== SESSION END ===
- Run: git status — check for uncommitted changes
- Run: git diff — review what changed this session
- Memory: if anything non-obvious was learned this session, save it to .claude/agent-memory/ for team sharing
==================
"""

print(REMINDER)
sys.exit(0)
