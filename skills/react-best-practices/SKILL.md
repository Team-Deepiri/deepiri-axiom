---
name: react-best-practices
description: >-
  React and Next.js performance optimization guidelines from Vercel Engineering.
  Use when writing, reviewing, or refactoring React/Next.js code — components,
  data fetching, bundle size, or performance.
allowed-tools: Read, Grep, Glob, WebFetch, TodoWrite
---

# React best practices (Vercel)

Performance guide for React and Next.js — ~70 rules across 8 categories, prioritized by impact.

Source: [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) (`react-best-practices`). MIT.

## When to apply

- New React components or Next.js pages
- Client or server data fetching
- Performance review / refactor
- Bundle size or load-time work

## Rule categories by priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Eliminating Waterfalls | CRITICAL | `async-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Server-Side Performance | HIGH | `server-` |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` |
| 5 | Re-render Optimization | MEDIUM | `rerender-` |
| 6 | Rendering Performance | MEDIUM | `rendering-` |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick reference

### 1. Eliminating waterfalls (CRITICAL)

- `async-cheap-condition-before-await` — cheap sync checks before await
- `async-defer-await` — await only in branches that need it
- `async-parallel` — `Promise.all()` for independent work
- `async-dependencies` — better-all for partial dependencies
- `async-api-routes` — start promises early, await late
- `async-suspense-boundaries` — Suspense to stream content

### 2. Bundle size (CRITICAL)

- `bundle-barrel-imports` — direct imports, avoid barrels
- `bundle-analyzable-paths` — static paths for smaller traces
- `bundle-dynamic-imports` — `next/dynamic` for heavy UI
- `bundle-defer-third-party` — analytics after hydration
- `bundle-conditional` — load only when feature is on
- `bundle-preload` — preload on hover/focus

### 3. Server-side (HIGH)

- `server-auth-actions` — auth server actions like API routes
- `server-cache-react` — `React.cache()` per-request dedupe
- `server-cache-lru` — LRU across requests
- `server-dedup-props` — avoid duplicate RSC serialization
- `server-hoist-static-io` — fonts/logos at module level
- `server-no-shared-module-state` — no mutable request state in RSC/SSR
- `server-serialization` — minimize client-bound data
- `server-parallel-fetching` — parallelize fetches in the tree
- `server-parallel-nested-fetching` — nested fetches in `Promise.all`
- `server-after-nonblocking` — `after()` for non-blocking work

### 4. Client data fetching (MEDIUM-HIGH)

- `client-swr-dedup` — SWR for request dedupe
- `client-event-listeners` — dedupe global listeners
- `client-passive-event-listeners` — passive scroll listeners
- `client-localstorage-schema` — version and minimize storage

### 5. Re-render (MEDIUM)

- `rerender-defer-reads` — don't subscribe for callback-only state
- `rerender-memo` — extract expensive memoized children
- `rerender-memo-with-default-value` — hoist default non-primitives
- `rerender-dependencies` — primitive effect deps
- `rerender-derived-state` — subscribe to derived booleans
- `rerender-derived-state-no-effect` — derive in render, not effects
- `rerender-functional-setstate` — functional setState for stable callbacks
- `rerender-lazy-state-init` — lazy `useState` init
- `rerender-simple-expression-in-memo` — skip memo for simple primitives
- `rerender-split-combined-hooks` — split independent hook deps
- `rerender-move-effect-to-event` — interaction logic in handlers
- `rerender-transitions` — `startTransition` for non-urgent updates
- `rerender-use-deferred-value` — defer expensive renders
- `rerender-use-ref-transient-values` — refs for transient values
- `rerender-no-inline-components` — no components defined inside components

### 6. Rendering (MEDIUM)

- `rendering-animate-svg-wrapper` — animate wrapper, not SVG
- `rendering-content-visibility` — `content-visibility` for long lists
- `rendering-hoist-jsx` — static JSX outside components
- `rendering-svg-precision` — reduce SVG precision
- `rendering-hydration-no-flicker` — inline script for client-only data
- `rendering-hydration-suppress-warning` — expected mismatches
- `rendering-activity` — Activity for show/hide
- `rendering-conditional-render` — ternary, not `&&`
- `rendering-usetransition-loading` — `useTransition` for loading
- `rendering-resource-hints` — React DOM resource hints
- `rendering-script-defer-async` — `defer` / `async` on scripts

### 7. JavaScript (LOW-MEDIUM)

- `js-batch-dom-css` — batch CSS via classes / `cssText`
- `js-index-maps` — Map for repeated lookups
- `js-cache-property-access` — cache props in loops
- `js-cache-function-results` — module-level result Map
- `js-cache-storage` — cache storage reads
- `js-combine-iterations` — one loop vs many filter/map
- `js-length-check-first` — length before expensive compare
- `js-early-exit` — return early
- `js-hoist-regexp` — RegExp outside loops
- `js-min-max-loop` — loop for min/max, not sort
- `js-set-map-lookups` — Set/Map O(1) lookups
- `js-tosorted-immutable` — `toSorted()` for immutability
- `js-flatmap-filter` — `flatMap` to map+filter
- `js-request-idle-callback` — idle-time non-critical work

### 8. Advanced (LOW)

- `advanced-effect-event-deps` — no `useEffectEvent` in effect deps
- `advanced-event-handler-refs` — handlers in refs
- `advanced-init-once` — init once per app load
- `advanced-use-latest` — `useLatest` for stable callback refs

## Deep dive (upstream rules)

Axiom installs a single file. For full incorrect/correct examples, WebFetch:

```
https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-best-practices/rules/<rule-id>.md
```

Compiled guide:

```
https://raw.githubusercontent.com/vercel-labs/agent-skills/main/skills/react-best-practices/AGENTS.md
```

## Handoff

- **performance-triage** — runtime latency after applying these patterns
- **code-review** — call out CRITICAL waterfall/bundle issues
