---
name: axiom-logging-standards
description: Structured logging conventions for Deepiri services.
---

# Axiom Logging Standards

Use when adding logging to a new code path or reviewing a PR's observability.

## Rules
- Structured (JSON or key-value), not free-text string concatenation — logs need to be queryable.
- Propagate request ID from gateway through every downstream log line for a given request.
- Log at the boundary of a decision (auth denied, rate limit hit, retry triggered), not just generic "processing request" noise.
- Never log secrets, tokens, or full request bodies containing user PII.
