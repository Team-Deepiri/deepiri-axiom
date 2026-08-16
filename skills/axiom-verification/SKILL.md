---
name: axiom-verification
description: Do not report a task done until the fix is confirmed against the real symptom, not just "it should work now."
---

# Axiom Verification

Triggers: about to say "fixed", "done", "should work", or hand back a task.

## Checklist before claiming completion
- Re-run the exact reproduction steps (or failing test) that proved the bug existed.
- For UI changes: actually load it and interact with the golden path, per this repo's own CLAUDE.md rule.
- For migrations: confirm against a real (or seeded) database, not just that Prisma generated cleanly.
- If verification isn't possible in this environment, say so explicitly — never claim success you didn't check.
