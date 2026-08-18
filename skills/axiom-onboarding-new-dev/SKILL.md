---
name: axiom-onboarding-new-dev
description: Fast-path checklist for a new Deepiri contributor's first week.
---

# Axiom Onboarding New Dev

Use when onboarding a new dev or QA engineer, or when asked "how do I get set up."

## Order
1. Clone `deepiri-platform` and relevant service repos; `./setup.sh` from `deepiri-axiom` for agent/skill install.
2. Read `docs/DOCUMENTATION_INDEX.md` and `docs/architecture/SYSTEM_ARCHITECTURE.md` before touching code.
3. Bring up the local Docker environment and confirm all containers report healthy.
4. Take a small, well-scoped first PR or QA review — not an open-ended "look around" task.

Point new QA engineers specifically at the `deepiri-qa-workflow` skill; point new devs at `axiom-writing-plans` and `axiom-tdd`.
