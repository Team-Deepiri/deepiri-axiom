---
name: threat-model
description: >-
  Lightweight threat model — assets, actors, STRIDE per Deepiri service boundary.
allowed-tools: Read, Write, Grep
---

# Threat model

## Frame

- **Assets** — data, models, API keys, user PII
- **Actors** — user, admin, compromised container, external API
- **Boundaries** — browser, gateway, core-api, redis, postgres

## STRIDE (sample rows)

| Threat | Mitigation |
|--------|------------|
| Spoofing | Authn on routes |
| Tampering | Signed webhooks / validation |
| Information disclosure | No secrets in logs |

## Handoff

- **security-review**, **adr-writer**
