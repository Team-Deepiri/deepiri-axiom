---
name: axiom-test-plan
description: Derive a test plan from a Deepiri PR diff — unit, integration, manual steps.
---

# Axiom Test Plan

Use when a PR lacks an explicit test plan, or when reviewing whether one is sufficient.

## Shape
1. **Unit** — what pure logic changed and what asserts it.
2. **Integration** — what service boundary or DB interaction needs a real (or realistic) dependency to verify.
3. **Manual** — what can only be checked by hand (UI, timing-sensitive behavior) and the exact steps to do it.

A test plan that only lists "ran the existing test suite" for a PR that adds new behavior is not a test plan — it needs a new test for the new behavior.
