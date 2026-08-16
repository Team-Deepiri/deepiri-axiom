---
name: axiom-database-migrations
description: Safe migration practice for Deepiri's per-service Postgres schemas (Prisma-based).
---

# Axiom Database Migrations

Use for any schema change in `deepiri-core-api` or another service's owned tables.

## Rules
- Migrations live in the **owning service only** — no cross-service migrations touching another service's schema.
- Additive first: new nullable columns before backfills before dropping old columns — never a single migration that both adds and removes in a way that breaks mid-deploy.
- Backfills run out-of-band from the migration itself for any non-trivial row count.
- State the rollback plan before merging, not after something breaks.
