---
name: axiom-security-review
description: Security pass for Deepiri services — auth order, injection, secrets, trust boundaries.
---

# Axiom Security Review

Use before merging anything touching auth, external input, or cross-service calls.

## Checklist
- Auth/authz runs **before** expensive work, not after.
- User input validated at every trust boundary (gateway, webhook ingress, form submission) — never trust a downstream service to re-validate.
- No secrets in code, logs, or committed `.env` — check `deepiri-wooven` patterns are followed.
- SQL/NoSQL queries are parameterized; no string-built queries from user input.
- Rate limits and request size limits exist on any newly exposed endpoint.

Flag anything that "would work" but bypasses gateway auth for convenience — that's the most common Deepiri-specific finding.
