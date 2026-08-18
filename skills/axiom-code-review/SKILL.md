---
name: axiom-code-review
description: Structured PR/code review — blocking vs important vs suggestion, with genuine praise.
---

# Axiom Code Review

Use for any Deepiri code review, human or AXIOM-assisted.

## Sections (in order)
1. **Blocking** — correctness, security, service-boundary violations, migration ownership. Must fix before merge.
2. **Important** — maintainability, missing test coverage, unclear naming. Should fix, negotiable timing.
3. **Suggestion** — style, minor refactors. Optional.
4. **Praise** — real, specific praise only — skip this section rather than pad it.

Check auth order, cross-service DB access, and migration ownership before anything else. Never approve on "looks fine" without reading the diff against its stated intent.
