---
name: composition-patterns
description: >-
  React composition patterns that scale. Use when refactoring boolean-prop
  proliferation, building flexible component libraries, or designing reusable
  APIs — compound components, render props, context providers, React 19 APIs.
allowed-tools: Read, Grep, Glob, WebFetch, TodoWrite
---

# Composition patterns (Vercel)

Flexible, maintainable React components via composition — not boolean prop sprawl.

Source: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (`composition-patterns`). MIT.

## When to apply

- Components with many boolean props
- Reusable component libraries
- Flexible component APIs
- Compound components / context providers
- Architecture review of React UI

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Architecture | HIGH | `architecture-` |
| 2 | State Management | MEDIUM | `state-` |
| 3 | Implementation Patterns | MEDIUM | `patterns-` |
| 4 | React 19 APIs | MEDIUM | `react19-` |

## Quick reference

### 1. Architecture (HIGH)

- `architecture-avoid-boolean-props` — don't customize via booleans; compose
- `architecture-compound-components` — shared context for complex components

### 2. State (MEDIUM)

- `state-decouple-implementation` — only the provider knows state plumbing
- `state-context-interface` — generic state / actions / meta for DI
- `state-lift-state` — state in providers for sibling access

### 3. Patterns (MEDIUM)

- `patterns-explicit-variants` — variant components over boolean modes
- `patterns-children-over-render-props` — children over `renderX` props

### 4. React 19+ (MEDIUM)

Skip if on React 18 or earlier.

- `react19-no-forwardref` — no `forwardRef`; prefer React 19 patterns (`use()` vs `useContext()`)

## Deep dive (upstream rules)

WebFetch detailed examples:

```
https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/composition-patterns/rules/<rule-id>.md
```

Compiled guide:

```
https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/composition-patterns/AGENTS.md
```

## Handoff

- **react-best-practices** — performance after structure is right
- **web-design-guidelines** — a11y/UX audit of composed UI
