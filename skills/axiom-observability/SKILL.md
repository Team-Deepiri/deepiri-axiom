---
name: axiom-observability
description: Logs, metrics, and health endpoints to check when a Deepiri service misbehaves.
---

# Axiom Observability

Use when debugging production behavior or reviewing a PR that touches a service's runtime path.

## What to check
- Health/readiness endpoints — do they check real dependencies (DB, Redis, Kafka) or just return 200 unconditionally?
- Structured logs — request ID propagation from gateway through to the owning service.
- Metrics — request latency, error rate, and queue depth for anything async (training jobs, Sorge bot runs).

A service with no health check that "passes" `docker compose up` healthy state is a false positive — verify the healthcheck actually exercises the dependency.
