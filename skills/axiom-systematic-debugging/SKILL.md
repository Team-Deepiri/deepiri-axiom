---
name: axiom-systematic-debugging
description: Generic 4-phase root-cause loop for any language or service, inside or outside AXIOM DEBUG mode.
---

# Axiom Systematic Debugging

Use for any bug hunt, not just Deepiri-flagged ones — this is the mechanics `axiom-debug` assumes you already know.

## Loop
1. **Reproduce** — get a minimal, reliable repro before touching code. No repro, no fix.
2. **Localize** — bisect the failure to the smallest unit (function, request hop, migration step) that still shows it.
3. **Hypothesize and falsify** — form one hypothesis at a time, find the test that would disprove it, run it. Do not stack unverified hypotheses.
4. **Fix at the root** — patch the cause, not the symptom; if the fix is a workaround, say so explicitly and file the real fix.

State confidence at each step: CERTAIN | HIGH | MODERATE | HYPOTHESIS | UNKNOWN. Never report a fix as done on a HYPOTHESIS-level root cause.
