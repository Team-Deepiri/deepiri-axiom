---
name: deepiri-gateway-auth
description: API gateway and auth-service trust boundary patterns.
---

# Deepiri Gateway Auth

Repos: `deepiri-api-gateway` (~5100), `deepiri-auth-service`.

- Gateway is the edge; auth runs before expensive downstream work.
- Never bypass gateway auth for “convenience” in internal calls from UI.
- Verify ports in compose / `.env` — do not invent defaults.
