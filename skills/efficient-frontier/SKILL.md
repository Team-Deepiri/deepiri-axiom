---
name: efficient-frontier
description: >-
  Orchestrate high-cost frontier models: keep planning, synthesis, tradeoffs,
  and final review on the expensive model; delegate research, coding, and
  testing to cheaper subagents for token-heavy work.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, TodoWrite, WebSearch, WebFetch
---

# Efficient frontier

Use the expensive model where judgment matters. Push repeatable, bounded, or token-heavy work to cheaper/faster subagents.

Source: [BuilderIO/skills](https://github.com/BuilderIO/skills) (`efficient-frontier`). MIT.

For Claude Fable specifically, prefer **efficient-fable**.

## Workflow

1. Frontier-only: architecture, prioritization, ambiguity, risk, synthesis, final review
2. Delegable: repo scans, search, docs extraction, testing passes, log reduction, narrow coding, mechanical edits
3. Spawn parallel subagents with clear ownership, bounded scope, verification gates, expected evidence
4. Require compact returns: findings, files, commands, residual risk, stop conditions, decisions needed
5. Integrate and review centrally before presenting

## Handoff packets

Self-contained prompts (assume no chat context): repo path, objective, scope, out-of-scope, targets, return format, verification commands, stop conditions.

Useful stops: code ≠ assumption; verification fails twice; needs files outside scope; no concrete evidence.

## Review loop

Treat delegated output as evidence, not verdict. Reopen cited files, skim high-risk diffs, spot-check verification. Resolve disagreements at the frontier layer.

## Soft scenarios

- **Research** — delegate scans/extraction; keep judgment
- **Coding** — bounded patches when ownership is clear; integrate centrally
- **Testing** — frontier chooses strategy; cheaper agents run checks/logs and return exact failures
- **Debugging** — independent theories in parallel; final diagnosis stays frontier

## Guardrails

- Do not delegate the immediate blocker you need next
- Do not have multiple agents edit the same files concurrently
- Do not trust high-risk conclusions blindly — inspect evidence
- Pattern works best when exploration/implementation can parallelize

## Default framing

Use the frontier model as orchestrator and reviewer; cheaper subagents for token-heavy research, coding, or testing so expensive tokens go to judgment and final quality.

## Handoff

- **efficient-fable** — same pattern when the orchestrator is Claude Fable
- **plow-ahead** — autonomy after the orchestration plan is set
- **agent-watchdog** — audit delegated agent output
- **stay-within-limits** — budget between parallel waves
