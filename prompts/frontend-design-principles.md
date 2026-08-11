# Frontend design principles (AXIOM)

Modern, maintainable frontends ship on **design tokens**, **system UIs**,
and **progressive enhancement** — not hard-coded hex values or framework
lock-in. Apply these rules to any Deepiri web surface (React/Vite studio apps,
Dash control rooms, vanilla viewers, generated HTML reports).

## 1. Design tokens first

- Define colors, typography, spacing, radii, shadows, and motion as CSS
  custom properties on `:root`.
- Parameterize **every** hard-coded color/radius/shadow into a variable.
  A rule of thumb: no literal `#` outside the token block.
- Provide a semantic palette (`--bg`, `--bg-card`, `--text`, `--muted`,
  `--border`, `--accent`, `--warn`, `--danger`, `--info`) plus soft
  variants (`--accent-soft`, `--danger-soft`) for tints.
- Set `color-scheme` so native controls and scrollbars match the theme.

## 2. Theme automatically

- Support **dark and light** via `@media (prefers-color-scheme: light)`
  that remaps the tokens (do not duplicate component rules).
- Keep contrast-accessible accents in both palettes; test light mode
  explicitly — it is the most commonly broken.

## 3. Fluid, responsive layout

- Use `clamp(min, preferred, max)` for type and hero sizes so text scales
  with viewport instead of jumping at breakpoints.
- Prefer `grid-template-columns: repeat(auto-fit, minmax(X, 1fr))` and
  **container queries** over single rigid breakpoints.
- Tables: wrap in an `overflow-x: auto` container; sticky headers only when
  the scroll container is the window/table.
- Mobile-first: collapse sidebars/stat rows before text gets cramped.

## 4. Motion, but not at the expense of usability

- Use `cubic-bezier` transitions (~150ms) on interactive elements and subtle
  elevation on hover/`:active` press feedback.
- Add `:focus-visible` outlines on every interactive element — keyboard users
  depend on them.
- Guard all animation with `@media (prefers-reduced-motion: reduce)`.

## 5. Component behavior

- Tabs, buttons, chips, and mode toggles share one base style plus
  `.-active`/`.-selected` modifiers; never re-declare base properties.
- Progress rings and bars should use CSS gradients/conic-gradients driven by
  CSS variables (`--pct`) rather than inline widths computed in JS.
- Keep JS for behavior; keep presentation in CSS.

## 6. Print & fallbacks

- Add `@media print` rules to reports/dashboards (remove shadows, unfix
  sticky headers, allow tables to lay out full width).
- When embedding third-party assets (CDN libs), pin versions and prefer
  modern ESM/import-map modules over old global builds.

## Rule

If a change leaves a hard-coded color, a fixed font size, or a media-query
layout that breaks at narrow widths, it is not finished. Verify by rendering
at desktop, tablet, mobile, and light mode before claiming the UI is modern.
