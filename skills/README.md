# Deepiri Axiom skills library

**73 packaged skills** installed by `./install.sh` into:

| Target | Path |
|--------|------|
| Cursor (project) | `.cursor/skills/<name>/SKILL.md` |
| Claude Code (project) | `.claude/skills/<name>/SKILL.md` |
| Cursor (global) | `~/.cursor/skills/<name>/SKILL.md` |

Regenerate static skills after editing the catalog:

```bash
python3 scripts/generate_skills.py
```

`deepiri-axiom` uses `SKILL.md.j2` for full prompt injection at install time.

## Categories

- **Platform** — gateway, auth, core-api, external-bridge, web-frontend, language-intelligence
- **AI runtime** — cyrex, persola, helox, modelkit, prismpipe, synapse, training, guardrails, toolbox
- **Infrastructure** — vizult, cascade, conduit, wooven, memorymesh, ollama, gpu/zepgpu
- **AXIOM modes** — scan, architect, debug, refactor, review
- **DX** — ecosystem, doc-grounding, service-boundaries, compose, skaffold, cross-repo
- **Products** — aarflingo, polylogue, sorge, boardman, huddle, tombstone, emotion, renderflow, egottol
- **Engineering practice** — axiom-systematic-debugging, axiom-tdd, axiom-verification, axiom-migration-safety, axiom-writing-plans, axiom-code-review, axiom-security-review, axiom-performance-triage, axiom-dependency-audit, axiom-secrets-hygiene, axiom-api-contract-design, axiom-database-migrations, axiom-caching-strategy, axiom-feature-flags, axiom-error-handling, axiom-logging-standards, axiom-test-plan, axiom-tech-debt, axiom-pr-description, axiom-adr-writing
- **Operations** — axiom-observability, axiom-incident-response, axiom-rate-limiting
- **DX** (cont.) — axiom-onboarding-new-dev
- **Research** — applied-math
- **QA** — deepiri-qa-workflow
