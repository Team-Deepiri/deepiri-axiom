---
name: axiom-error-handling
description: Consistent error surfaces and failure handling across Deepiri services.
---

# Axiom Error Handling

Use when reviewing or writing error paths, not just happy-path logic.

## Rules
- Errors crossing a service boundary get a structured shape (code, message, optionally a trace ID) — not a raw stack trace or a bare string.
- Distinguish retryable from non-retryable errors explicitly; callers need to know which is which.
- Never swallow an exception silently to "keep things running" — log it with enough context to actually debug later, or let it propagate.
