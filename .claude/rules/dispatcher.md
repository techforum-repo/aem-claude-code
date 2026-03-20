---
description: Rules for Dispatcher configuration and domain setup — vhost/farm patterns, etc/map JCR mappings, rewrite rules, security filters, caching, and Cloud Manager compatibility
paths:
  - "dispatcher/src/**/*.conf"
  - "dispatcher/src/**/*.any"
  - "dispatcher/src/**/*.vhost"
  - "dispatcher/src/**/*.farm"
  - "ui.content/**/etc/map*/**"
---

# Instructions for Dispatcher configuration and domain setup

## Scope
Use this guidance for Dispatcher configuration and the full domain setup workflow: vhost, farm, JCR etc/map, and rewrite rules.

## Complete domain setup checklist

When adding a new domain, **all four of these must be done together**:

1. Vhost in `dispatcher/src/conf.d/available_vhosts/`
2. Farm in `dispatcher/src/conf.dispatcher.d/available_farms/`
3. Symlinks in the corresponding `enabled_*` directories
4. **JCR etc/map entry** in `ui.content/src/main/content/jcr_root/etc/map.publish/`

Never do one without the others unless explicitly asked.

## vhost and farm setup pattern

- Always create files in `available_*`, never directly in `enabled_*`.
- Symlink to enable using relative paths:
  ```bash
  cd dispatcher/src/conf.d/enabled_vhosts && ln -s ../available_vhosts/<name>.vhost <name>.vhost
  cd dispatcher/src/conf.dispatcher.d/enabled_farms && ln -s ../available_farms/<name>.farm <name>.farm
  ```
- For domain-specific farms, list hostnames inline in `/virtualhosts` (not via `$include`):
  ```
  /virtualhosts {
    "www.example.com"
    "example.com"
  }
  ```
- Never edit `default.vhost` or `default.farm` — these are SDK reference files.
- Remind the user to add `/etc/hosts` entries for local testing:
  ```
  127.0.0.1   www.example.com example.com
  ```

## JCR etc/map pattern

AEM uses Sling URL mapping under `/etc/map.publish/` (publish) and `/etc/map.author/` (author) to resolve short URLs to content paths.

**Always read the existing entries** in `ui.content/src/main/content/jcr_root/etc/map.publish/` before creating a new one — match the exact folder structure, node types, and property names already in use.

**Typical structure** (adapt to what exists in the project):
```
ui.content/src/main/content/jcr_root/etc/
└── map.publish/
    └── .content.xml              ← root mapping node
    └── http/
        └── .content.xml
        └── www.example.com.80/   ← one folder per domain+port
            └── .content.xml
    └── https/
        └── .content.xml
        └── www.example.com.443/
            └── .content.xml
```

**Domain folder `.content.xml` pattern** (match existing entries exactly):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0"
          xmlns:jcr="http://www.jcp.org/jcr/1.0"
    jcr:primaryType="sling:Mapping"
    sling:match="www.example.com.80/"
    sling:internalRedirect="/content/my-site/"/>
```

**Key properties:**
- `jcr:primaryType="sling:Mapping"` — always required
- `sling:match` — the incoming host+port pattern (e.g. `www.example.com.80/`)
- `sling:internalRedirect` — maps to the JCR content path (e.g. `/content/my-site/`)
- Use `sling:redirect` instead of `sling:internalRedirect` only for external redirects (rare)

**Always create entries for both HTTP (port 80) and HTTPS (port 443)** unless the project only uses one protocol.

## Rewrite rules

- Rewrite rules in `conf.d/rewrites/rewrite.rules` apply globally across all enabled vhosts.
- The content mapping rule (`RewriteRule ^/(.*)$ /content/${CONTENT_FOLDER_NAME}/$1`) uses the global `CONTENT_FOLDER_NAME` variable — if a new domain serves different content, add a domain-specific `RewriteCond %{HTTP_HOST}` guard or define a separate variable.
- The root redirect (`/` → `/us/en.html`) applies to all vhosts — adjust if a new domain needs a different entry point.
- Add per-domain rewrites under a `RewriteCond %{HTTP_HOST}` guard to avoid affecting other vhosts.

## Security filter rules

- `/filter` should default deny; allow only explicitly required paths.
- Block or tightly restrict sensitive AEM endpoints: `/crx`, `/system`, `/bin/wcmcommand`, `/bin/receive`, `/etc/replication`, `/mnt/overlay`, `/editor.html`, and CF authoring routes (`/assets.html`, `/mnt/overlay/dam/cfm`).
- Restrict `.json` and `.infinity.json` exposure unless a specific public use case exists.
- Ensure required security headers are present where the repository manages them.

## Caching rules

- Never cache authenticated, personalized, or user-specific responses.
- Use `/ignoreUrlParams` to avoid cache fragmentation from analytics-style query parameters.
- Keep cache invalidation rules aligned with actual publish flush behavior.
- Use only Dispatcher directives supported by the AEMaaCS Dispatcher SDK.

## Review focus

- All four domain setup steps completed together (vhost, farm, symlinks, etc/map)
- etc/map entries match existing project structure and node types
- Both HTTP and HTTPS mapping entries created
- `available_*/enabled_*` symlink pattern followed
- Inline `/virtualhosts` for domain-specific farms
- Rewrite rules guarded per-domain where needed
- `/etc/hosts` reminder given for local dev
- Default-deny filter posture
- Exposure of sensitive endpoints or JSON data
- Security header coverage
- Caching of authenticated or personalized content
- Dispatcher SDK and Cloud Manager compatibility
