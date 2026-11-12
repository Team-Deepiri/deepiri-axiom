---
name: plan-arbiter
description: >-
  Compare, cross-review, merge, judge, or choose among competing plans from
  multiple agents (pasted strategies, plan docs, PR descriptions, transcripts).
  Produce one recommended execution plan with verification gates.
allowed-tools: Read, Grep, Glob, WebSearch, WebFetch, TodoWrite
---

# Plan arbiter

Turn competing plans into one executable direction. Preserve best ideas; reject weak assumptions; avoid blended mush.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`plan-arbiter`). MIT.

Planning is **read-only** unless the user explicitly asks to implement after the decision.

## Workflow

1. Collect source plans
2. Normalize into comparable claims
3. Cross-review against each other and the real codebase/task
4. Adopt, hybridize, or send back for revision
5. One execution handoff with verification gates and rejected alternatives

## Collect

Accept pasted text, files, transcripts, PRs, comments, or chat history. Resolve originals when possible. If still writing and user asked to wait, monitor until done/blocked. Mark unresolved sources as risk.

## Normalize (per plan)

- Objective and scope
- Assumptions and open questions
- Proposed files/modules/APIs/data/UI/workflows
- Implementation sequence
- Validation strategy
- Rollback / migration concerns
- Cost, complexity, executor fit

Prefer concrete, grounded, honest plans over verbosity.

## Cross-review

- Satisfies the actual request?
- Claims match repo/docs/tests when available?
- Hidden deps, missing tests, risky sequencing, vague steps, excess scope?
- Complementary strengths across plans?
- Separate plan quality from which model should *execute*

Use subagents for large plans or separate technical vs product passes.

## Decide

- **Adopt** — one plan mostly as written
- **Hybrid** — combine specific pieces
- **Revise first** — both miss a key constraint

Tie-break: (1) correctness/fit (2) grounding (3) simpler first step that doesn't block the future (4) better validation/rollback (5) lower execution cost once quality is ok

## Handoff memo

```md
Decision
- Adopt Plan A / Hybrid / Revise first.

Why
- Deciding evidence and tradeoffs.

Execution Plan
- Ordered steps with files or surfaces to touch.

Borrowed From Other Plans
- Useful pieces kept from non-winning plans.

Rejected
- Ideas intentionally not taking, with reasons.

Verification
- Tests, checks, review, or deploy gates needed.

Executor Recommendation
- Which agent/model should implement and why.
```

If the user already asked for execution and the path is clear, report the decision briefly then proceed. Otherwise stop for approval.

## Handoff

- **plow-ahead** — execute the chosen plan autonomously
- **ship** / **mvp** — shrink scope before coding
