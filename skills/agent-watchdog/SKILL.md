---
name: agent-watchdog
description: >-
  Watch, babysit, audit, review, compare, or fix another agent's work from a
  session, transcript, PR, branch, log, or pasted run summary. Reconstruct the
  ask, inspect changes and verification, report gaps, optionally make scoped
  fixes when authorized.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, WebFetch
---

# Agent watchdog

Reviewer with a pager: wait for completion when needed, reconstruct the request, verify evidence, close the gap between ask and outcome.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`agent-watchdog`). MIT.

## Modes

- **Watch only** — monitor until terminal state; no edits
- **Audit** — gap report from prompt/transcript/diff/tests/CI; no edits
- **Audit and fix** — audit first, then narrow fixes for clear gaps
- **Compare** — multiple sessions/agents against the same original request

If authority is unclear, default to audit-only and say what you would fix.

## Resolve the target

1. Identify artifacts: session ID, transcript, PR, branch, CI, pasted summary
2. Prefer the most direct source over summaries
3. If still running and user asked to watch, poll until done/blocked/stale
4. If unresolvable, ask for the missing identifier

## Reconstruct the contract

- Original request and later scope changes
- Explicit constraints (branch, no-edit, validation, security)
- Implied acceptance criteria (behavior, tests, CI, docs, screenshots)
- Other agent's final claims and caveats

User request is source of truth — not the other agent's summary.

## Audit evidence

- Changed files + relevant neighbors
- git status/diff without reverting unrelated work
- Claimed commands vs actual output when available
- Failed/skipped tests, CI, screenshots, review threads
- UI: prefer screenshots/browser over prose claims

Classify: **Gap** | **Bug** | **Verification miss** | **Scope drift** | **No issue**

## Fix narrowly (when authorized)

1. Only clear-evidence gaps
2. Preserve unrelated local changes; no branch moves unless asked
3. Existing patterns + targeted tests
4. Smallest validation after each meaningful fix
5. Stop for product decisions, credentials, destructive or broad rewrites

## Report

```md
Status
- Done, blocked, stale, or still running.

Requested
- What the user asked the watched agent to do.

Observed
- What changed, claimed, and verified.

Gaps
- Missing behavior, bugs, weak verification, or scope drift.

Fixes made
- Files changed and validation. Omit for audit-only.

Remaining risk
- Still unverified or waiting on CI/review/human.
```

## Handoff

- **code-review** / **security-review** — deeper specialized passes
- **plan-arbiter** — if competing agent plans need a decision, not a fix
