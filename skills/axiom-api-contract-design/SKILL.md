---
name: axiom-api-contract-design
description: Define or review API contracts between Deepiri services (gateway, core-api, Cyrex, etc.).
---

# Axiom Api Contract Design

Use when adding or changing an endpoint another service depends on.

## Checklist
- Version the contract if the change isn't backward compatible — don't silently break existing callers.
- State the error shape explicitly, not just the happy path.
- Confirm the gateway's routing/middleware config is updated in the same change, not a follow-up.
- Cross-service contracts get documented in `docs/architecture/` — a contract only living in code is a contract nobody else can review.
