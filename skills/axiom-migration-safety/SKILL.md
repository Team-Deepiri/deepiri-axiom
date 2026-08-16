---
name: axiom-migration-safety
description: Prisma migration checklist enforcing per-service schema ownership across Deepiri's Node services.
---

# Axiom Migration Safety

Applies to `deepiri-core-api`, `deepiri-auth-service`, `deepiri-external-bridge-service`, `deepiri-language-intelligence-service` — each owns its own Postgres schema and Prisma migrations.

## Checklist
- Never write a migration for a table owned by another service — cross-service data flows over HTTP/queue, never a shared migration.
- Additive first: new nullable columns / new tables before any destructive `DROP`/`NOT NULL` tightening.
- Backfills run as a separate step from schema change on tables with meaningful production rows; check locking behavior under concurrent writes.
- Verify the migration against a local or seeded Postgres, not just `prisma generate` succeeding.
- Note rollback: can this migration be reverted without data loss? If not, say so before merging.
