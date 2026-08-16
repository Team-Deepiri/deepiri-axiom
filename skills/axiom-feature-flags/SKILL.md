---
name: axiom-feature-flags
description: Feature flag conventions for safe, reversible Deepiri rollouts.
---

# Axiom Feature Flags

Use when shipping anything risky enough to want a kill switch.

## Rules
- Flag the smallest reversible unit of behavior, not an entire feature — coarse flags force all-or-nothing rollback.
- Default flags to **off** in shared config; never rely on a hardcoded default buried in application code.
- Remove the flag and its dead branch once the rollout is confirmed stable — a permanent flag is tech debt, not a feature.
