---
description: Accessibility rules for AEM components — WCAG 2.1 AA compliance in HTL, Coral UI dialogs, and frontend markup
paths:
  - "ui.apps/**/*.html"
  - "ui.apps/**/*.xml"
  - "ui.frontend/**/*.html"
  - "ui.frontend/**/*.js"
  - "ui.frontend/**/*.jsx"
  - "ui.frontend/**/*.ts"
  - "ui.frontend/**/*.tsx"
  - "ui.frontend.react/**/*.jsx"
  - "ui.frontend.react/**/*.tsx"
  - "ui.frontend.spa/**/*.jsx"
  - "ui.frontend.spa/**/*.tsx"
---

# Accessibility rules

## Target standard

AEMaaCS projects must meet **WCAG 2.1 Level AA**. Apply these rules to all HTL templates, Coral UI dialog definitions, and frontend components.

## HTL templates

- Every `<img>` must have an `alt` attribute — derive it from an authored field, not hardcoded text. For decorative images, set `alt=""` and add `role="presentation"`.
- Interactive elements (`<a>`, `<button>`) must have visible text or an `aria-label`. Avoid icon-only buttons without a screen-reader label.
- Use semantic HTML first (`<nav>`, `<main>`, `<article>`, `<section>`, `<header>`, `<footer>`) before adding ARIA roles.
- Do not use ARIA roles to override native semantics when the correct element exists (e.g. use `<button>` not `<div role="button">`).
- Form inputs must have associated `<label>` elements or `aria-labelledby` references.
- Heading levels must be logical — do not skip from `<h2>` to `<h4>` to achieve visual styling; use CSS instead.
- Landmark regions (`<main>`, `<nav>`, etc.) must be unique or distinguished with `aria-label` when multiple of the same type exist on a page.
- Focus must remain visible — do not suppress the focus ring with `outline: none` without a custom focus indicator.
- Dynamic content changes (carousels, tab panels, dialogs) must use `aria-live` or role-appropriate patterns (`role="dialog"`, `aria-expanded`, `aria-selected`).

## Coral UI dialogs (`_cq_dialog/.content.xml`)

- Every dialog field must have a non-empty `fieldLabel` — this label appears in authoring and is required for accessibility in the Author UI.
- Provide `fieldDescription` for fields that need authoring guidance — do not rely only on placeholder text.
- When adding new dialog fields, do not remove or rename existing fields without checking for authored content impact — renamed fields silently lose their values.

## Frontend components (React / SPA)

- Images rendered via React or SPA must pass `alt` through props — do not default to an empty string silently.
- Modal dialogs must trap focus and restore focus to the trigger on close; use `aria-modal="true"` and `role="dialog"` with `aria-labelledby`.
- Tab or accordion components must implement keyboard navigation (`ArrowLeft`/`ArrowRight` for tabs, `Enter`/`Space` for toggle).
- Custom interactive components that do not use native HTML controls must be keyboard-operable and have appropriate ARIA roles and states.
- Do not rely on color alone to convey information — pair color cues with text, icons, or patterns.

## Review focus

- `<img>` without `alt`, or `alt` hardcoded to a non-descriptive string like the file name
- Icon-only interactive elements with no `aria-label`
- Non-semantic `<div>`/`<span>` used for interactive behavior
- Dialog fields with empty or missing `fieldLabel`
- Heading levels that skip or are chosen for visual weight rather than document structure
- Focus ring removal without a visible custom replacement
- Dynamic content with no `aria-live` or role-based announcement
- SPA modal components with no focus trap or focus restoration
