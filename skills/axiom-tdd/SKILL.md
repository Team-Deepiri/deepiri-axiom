---
name: axiom-tdd
description: RED-GREEN-REFACTOR discipline for new code across Node, Python, Go, and Rust Deepiri services.
---

# Axiom Tdd

Use when adding new behavior, not when characterizing legacy code (write characterization tests first there instead).

## Loop
1. **RED** — write a failing test that encodes the requirement, run it, confirm it fails for the expected reason.
2. **GREEN** — write the minimum code to pass. No extra abstraction, no speculative generality.
3. **REFACTOR** — clean up with the safety net green; re-run tests after every structural change.

Match the owning service's existing test runner (`pytest`, `jest`/`vitest`, `go test`, `cargo test`) — don't introduce a new one for a single feature.
