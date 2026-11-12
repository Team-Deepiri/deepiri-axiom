---
name: efficient-fable
description: >-
  Use when running Claude Fable on codebase-heavy or token-heavy work and the
  user wants Fable to orchestrate research, coding, and testing while cheaper
  subagents do bounded heavy lifting.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, WebSearch, WebFetch
---

# Efficient Fable

Use Claude Fable as the orchestrator, architect, synthesizer, and final judge. Use cheaper subagents for token-heavy research, coding, testing, and summarization that do not need Fable's full judgment.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`efficient-fable`). MIT.

For the same pattern on any frontier model (not Fable-specific), use **efficient-frontier**.

## Where Fable shines

Reserve Fable for:

- Decomposing ambiguous work into clean parallel slices
- Architecture, product, and safety tradeoffs
- Reading conflicting subagent reports and deciding what matters
- Integrating partial implementations into one coherent plan
- Final review, risk assessment, and user-facing synthesis

## Delegation pattern

1. Name the expensive-token risk: large repo search, long logs, broad docs, or repetitive edits
2. Split independent work into subagents before reading everything yourself
3. Use cheaper models for research scans, inventory, search summaries, narrow bug hunts, browser/testing passes, test output reduction, and bounded code edits
4. Ask subagents for concise evidence: files, line refs, commands run, diffs, uncertainties, and stop conditions
5. Spend Fable tokens on the decision layer: compare results, resolve conflicts, choose the path, review the final patch

Prefer parallel subagents when slices are independent. Keep blocking or highly coupled work local.

## Handoff packets

Write delegated prompts as if the subagent has no chat context. Include:

- Repo path and exact objective
- In-scope / out-of-scope files, packages, or surfaces
- Evidence format: files, line refs, commands, diffs, failures, uncertainty
- Verification commands or flows, plus what success looks like when known
- Stop conditions: code ≠ prompt assumption, command fails after a reasonable retry, or out-of-scope files needed → stop and report

## Vetting delegated work

Treat subagent reports as leads, not facts. Before high-impact use, a PR, or telling the user work is done: reopen cited files, confirm line refs/failures, review the final diff against the task. Lighter agents gather signal; Fable keeps truth-judgment.

## Soft scenarios

- **Research** — lighter agents scan docs/APIs/repo; Fable decides what changes the plan
- **Coding** — cheaper agents do bounded edits; Fable owns shared-file coordination, integration, final review
- **Testing** — Fable picks validation strategy; lighter agents run tests/browser/logs and report exact failures + flaky vs real
- **Debugging** — cheaper agents cluster logs/repro/small fixes; Fable picks the trustworthy diagnosis

If the task is tiny or validation itself needs delicate judgment, keep it with Fable.

## Guardrails

- Do not delegate the immediate blocker you need next
- Do not have multiple agents edit the same files concurrently
- Do not trust high-risk conclusions blindly — inspect evidence
- Pattern works best when exploration/implementation can parallelize

## Handoff

- **efficient-frontier** — same orchestration for non-Fable frontier models
- **agent-watchdog** — audit delegated agent output
- **stay-within-limits** — budget between parallel waves
- **plow-ahead** — autonomy after the orchestration plan is set
- **quick-recap** — 🟢/🟡/🔴 at end of a wave
