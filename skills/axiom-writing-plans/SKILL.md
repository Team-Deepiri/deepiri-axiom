---
name: axiom-writing-plans
description: Structured implementation plans with explicit human checkpoints for multi-file or cross-repo Deepiri changes.
---

# Axiom Writing Plans

Use before starting any change that spans more than one file with non-obvious ordering, or touches more than one Deepiri repo.

## Plan shape
1. **Goal** — one sentence, the observable outcome.
2. **Steps** — ordered, each naming the file/repo it touches and why that order matters (e.g., shared lib bump before dependents via `deepiri-cascade`).
3. **Checkpoints** — where you stop and confirm with the user before continuing (schema changes, anything touching `main`, anything crossing service boundaries).
4. **Verification** — how each step will be confirmed (test command, manual repro, migration check).

Keep it as a plan artifact the user approves, not prose buried in a chat reply — pair with `executing-plans` for the run.
