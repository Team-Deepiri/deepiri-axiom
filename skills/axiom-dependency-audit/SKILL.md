---
name: axiom-dependency-audit
description: Audit Python/Node/Go/Rust dependencies across Deepiri repos — outdated, CVEs, license conflicts.
---

# Axiom Dependency Audit

Use before a release or when `deepiri-cascade` flags a version drift.

## Checklist
- Run the ecosystem's native audit tool (`npm audit`, `pip-audit`, `cargo audit`, `govulncheck`) — don't eyeball versions.
- Cross-check any shared lib bump (`deepiri-modelkit`, `deepiri-shared-utils`) against every dependent via `deepiri-cascade` before merging.
- Flag license changes on new dependencies, not just CVEs.

A clean audit on one repo with an un-bumped shared dependency elsewhere is not actually clean — check the dependents.
