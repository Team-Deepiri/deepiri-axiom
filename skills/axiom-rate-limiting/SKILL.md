---
name: axiom-rate-limiting
description: Rate limit design at the Deepiri API gateway and per-service edges.
---

# Axiom Rate Limiting

Use when adding a new public or cross-service endpoint.

## Checklist
- Rate limit at the gateway first — don't rely solely on downstream services to self-protect.
- Distinguish per-user, per-IP, and per-service-caller limits; they usually need different thresholds.
- Return a clear 429 with retry-after, not a silent drop or generic 500.

Endpoints fronting expensive work (model inference, training triggers) need tighter limits than read-only endpoints.
