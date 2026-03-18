---
description: Rules for AEM integration tests (it.tests) and UI tests (ui.tests) — Cloud Manager pipeline structure, test authoring, and environment handling
paths:
  - "it.tests/src/**/*.java"
  - "ui.tests/src/**/*.java"
  - "ui.tests/src/**/*.ts"
  - "ui.tests/src/**/*.js"
---

# Integration and UI test rules

## Cloud Manager pipeline stages

- **Integration tests** (`it.tests`) — run after deployment against a live AEM environment in Cloud Manager. Use the Sling Testing Client or AEM Testing Clients.
- **UI tests** (`ui.tests`) — run against the published environment using a browser automation framework (Cypress or Selenium/WebDriver).
- Both stages are required for Cloud Manager production pipeline promotion — missing or all-skipped tests can block the pipeline.

## Integration tests (`it.tests`)

- Extend `com.adobe.cq.testing.client.CQClient` or use `SlingClient` for HTTP-based tests
- Read environment from system properties — never hardcode URLs, credentials, or ports:
  ```java
  String authorUrl = System.getProperty("it.author.url");
  String adminPassword = System.getProperty("it.author.password");
  ```
- Use `@RunWith(Parameterized.class)` with `BasicCredentials` for author/publish matrix testing
- Clean up any content created during the test — use `@After` to delete test nodes
- Do not use `Thread.sleep()` — use `Polling` or retry mechanisms from the testing client library
- Mark tests that must not run in Cloud Manager with `@Ignore` and a clear explanation

## UI tests (`ui.tests`)

- Tests run inside a Docker container in Cloud Manager — use relative URLs, not hardcoded hostnames
- Read the base URL from environment variables: `AUTHOR_URL`, `PUBLISH_URL`, `AEM_AUTHOR_PASSWORD`
- Use page object patterns — keep selectors out of test logic
- Avoid hard waits (`cy.wait(5000)`) — use element existence or network idle assertions
- Test meaningful authoring or delivery flows, not component styling details
- Keep tests independent — each test must be runnable in isolation

## Review focus

- hardcoded URLs, hostnames, or credentials
- missing environment variable reads
- tests that leave content behind after execution
- `Thread.sleep()` or hard waits instead of polling/retries
- tests that always pass regardless of AEM state (no real assertions)
- UI test selectors tied to CSS class names likely to change
