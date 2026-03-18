---
description: Security rules for Java files in core — servlets, filters, services, workflow steps
paths:
  - "core/src/main/**/*.java"
---

# Security instructions for Java files in `core`

## Scope
Apply these rules to servlets, filters, services, workflow steps, schedulers, and any Java code that handles repository access or request input.

## Key rules
- Use `resourceResolverFactory.getServiceResourceResolver(...)` with a named subservice when repository access is required.
- Keep service user mappings and ACL provisioning in `ui.config`; do not attempt to create them in Java code.
- Never concatenate untrusted input into JCR-SQL2, XPath, LDAP, or similar query strings.
- Validate path-based input before passing it to repository lookup APIs.
- Do not expose stack traces, internal repository paths, or sensitive details in responses or logs.
- Prefer resource type servlet registration over path-based registration unless an existing repository pattern requires otherwise.
- Treat path-based servlets as publicly reachable and ensure access control and dispatcher filtering are considered.
- Flag hardcoded credentials, tokens, or secrets immediately.

## Review focus
- unsafe resolver or subservice usage
- query construction from user input
- unvalidated path input
- path-based servlet exposure
- sensitive data leakage in logs or responses
- hardcoded secrets or credentials
