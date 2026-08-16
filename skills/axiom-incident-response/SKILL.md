---
name: axiom-incident-response
description: Contain, diagnose, communicate, postmortem for a Deepiri production incident.
---

# Axiom Incident Response

Use when a service is down or degraded in production, not for routine bugs.

## Order
1. **Contain** — can the blast radius be limited (feature flag, rollback, circuit-break the failing dependency) before root-causing?
2. **Diagnose** — logs + metrics from the owning service first, then upstream/downstream. Don't guess before checking.
3. **Communicate** — status update to affected stakeholders before the fix is fully verified, not after.
4. **Postmortem** — root cause, timeline, and one concrete prevention action — not a vague "add more monitoring."
