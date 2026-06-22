---
name: deepiri-service-boundaries
description: Enforce Deepiri microservice ownership and trust boundaries.
---

# Deepiri Service Boundaries

Non-negotiable:
- Each service owns its Postgres schema + Prisma migrations.
- Cross-service data via HTTP, queues, or streams — never shared DB reads.
- Gateway + auth validate **before** heavy handlers.
- Route changes to the **owning repo**; state blast radius.
