---
name: axiom-performance-triage
description: Latency and throughput triage across Deepiri's Redis, Ollama, Postgres, and gateway hops.
---

# Axiom Performance Triage

Use when a service is slow, not just broken.

## Triage order
1. Reproduce with a timing measurement, not a feeling.
2. Profile the hot path — is it the DB query, the gateway hop, model inference, or serialization?
3. Check for N+1 queries and missing indexes before reaching for caching.
4. If adding caching (`deepiri-memorymesh` or a local cache), state the invalidation strategy explicitly — stale-cache bugs are worse than the latency they fix.

Don't optimize the wrong hop — measure before changing code.
