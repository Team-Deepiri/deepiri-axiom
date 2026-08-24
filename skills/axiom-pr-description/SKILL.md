---
name: axiom-pr-description
description: Write a Deepiri PR title and body from the branch's actual commits and diff.
---

# Axiom Pr Description

Use before opening a PR, or when reviewing one with a thin description.

## Shape
- **Summary** — 1-3 bullets on what changed and why, not a restatement of the diff.
- **Test plan** — see `axiom-test-plan`; link it rather than duplicating.
- Link related PRs or issues, especially cross-repo companions (e.g. a `deepiri-cascade`-driven dependent bump).

A PR description that says "see commits" is not a description — read the actual diff and summarize its effect, not its mechanics.
