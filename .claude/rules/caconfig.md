---
description: Rules for Sling Context-Aware Configuration — structure, placement, and Java integration
paths:
  - "ui.content/**/sling:configs/**/*.xml"
  - "core/src/main/**/*Config*.java"
  - "core/src/main/**/*Configuration*.java"
  - "ui.config/**/caconfig/**/*.xml"
---

# Sling Context-Aware Configuration (CAConfig) rules

## When to use CAConfig vs OSGi config

- Use **CAConfig** for site-specific or environment-neutral settings that authors or operations may need to change per content tree (e.g. API endpoint per site, feature flags per country)
- Use **OSGi config** for infrastructure settings that are environment-specific (e.g. timeouts, credentials, thread pool sizes)
- Do not duplicate the same setting in both — pick one owner

## Configuration interface

- Define configs as a `@interface` annotated with `@Configuration` (`org.apache.sling.caconfig.annotation.Configuration`)
- Set `name` and `label` on `@Configuration` — these appear in the CAConfig editor
- Every field must have a default — CAConfig resolution can return the interface default if no config exists
- Use `@Property` to add labels and descriptions visible in the UI

## Java usage

- Inject via `@Self` on a Sling Model: `@Self private ConfigurationBuilder configurationBuilder;`
- Resolve with `configurationBuilder.as(MyConfig.class)` — never cast or use raw `ValueMap`
- Always handle the case where no configuration exists — the returned object uses defaults but is never null
- Do not cache the resolved config across requests — resolve it fresh in `@PostConstruct`

## Content placement

- Store config nodes under `/conf/<project>/sling:configs/<config-name>` in `ui.content`
- Inherit order: resource → `/conf/<site>` → `/conf/global` → defaults
- Use `sling:configRef` on the content root to point to the correct `/conf` bucket

## Review focus

- Is the `@Configuration` interface placed in `core` and not in a UI module?
- Are defaults defined for every field to handle missing config gracefully?
- Is the config resolved per request (not cached in a singleton field)?
- Is the config node placed in `ui.content` under `/conf`?
- Is `sling:configRef` set on the content root to wire up inheritance?
