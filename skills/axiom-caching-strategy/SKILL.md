---
name: axiom-caching-strategy
description: Choosing what to cache, where, and how it invalidates across the Deepiri stack.
---

# Axiom Caching Strategy

Use when performance work reaches for a cache instead of fixing the underlying query/hop.

## Questions to answer before adding a cache
- What invalidates it, and is that path actually wired up, or assumed?
- Is staleness acceptable for this data, and for how long?
- Local process cache, Redis, or `deepiri-memorymesh` — which fits the sharing scope needed?

A cache with no invalidation path is a bug generator, not a performance fix — write the invalidation trigger in the same change as the cache.
