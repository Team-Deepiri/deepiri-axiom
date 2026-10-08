---
name: plow-ahead
description: >-
  Autonomous progress without routine clarification stops. Use for "plow ahead",
  "do not stop", "use your best judgment", "keep going until done", "finish
  while I am away", or "do not ask unless truly blocked". State assumptions,
  proceed, validate, stop only for true blockers, end with a decision recap.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, WebSearch, WebFetch
---

# Plow ahead

Proceed through ordinary ambiguity. Make reasonable assumptions, keep momentum, validate as you go, and recap decisions clearly.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`plow-ahead`). MIT.

## Autonomy contract

- Turn routine questions into explicit assumptions
- Prefer the smallest reversible choice that satisfies the request
- Use repo conventions, nearby patterns, local docs, and tests as the decision source
- Keep working through normal test failures, missing context, and minor ambiguity
- Use subagents for independent research/implementation/verification when helpful
- Do not pause merely to ask which reasonable option the user prefers

## Stop conditions (ask only then)

- Missing credentials, secrets, accounts, paid services, or private data
- Destructive, irreversible, or production-mutating next step
- Branch rewrite, force push, or deletion not explicitly requested
- High legal/safety/privacy/security risk with no safe local choice
- User reserved the decision
- Verification fails repeatedly and the next fix would be speculative

If blocked: self-contained handoff — done, blocker, exact input needed, next inspect target.

## Decision rules

1. Reuse patterns before inventing
2. Local, reversible, low blast radius
3. Tight scope to the request
4. Correctness/maintainability over cleverness
5. Smallest meaningful validation first
6. If close, pick the option easier to review later

Keep a lightweight decision log (notes or final answer); no new repo artifact unless needed.

## Work loop

1. Restate goal and acceptance criteria
2. Inspect real files/docs/runtime before editing
3. State assumptions, then act
4. Implement in small coherent steps
5. Targeted validation; fix failures
6. Repeat until done or stop condition
7. Review diff + evidence against the original request

## Final recap

```md
Goal
- What you completed.

Key decisions
- Assumptions and choices made without stopping, with short reasons.

Changes
- Files, behavior, docs, or configuration changed.

Validation
- Commands, tests, or checks run and their result.

Remaining risk
- Anything not verified, deferred, or blocked.
```

## Handoff

- **quick-recap** — end with 🟢/🟡/🔴 status
- **ship** — when weekend scope still applies under autonomy
