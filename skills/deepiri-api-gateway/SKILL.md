---
name: deepiri-api-gateway
description: Route design, proxy rules, and edge concerns for deepiri-api-gateway.
---

# Deepiri Api Gateway

Owns: routing to core-api, auth, external-bridge, language-intelligence.

Check: middleware order, rate limits, request ID propagation, CORS, health checks.
Document any new upstream in gateway config + `docs/architecture/`.
