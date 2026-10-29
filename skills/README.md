# Deepiri Axiom skills library

**113 packaged skills** installed by `./install.sh` into:

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
- **Company discovery** — ult-quo-company (Quo-pattern Deepiri software domains; no hardware)
- **QA** — deepiri-qa-workflow

## Synced from exovra-jayden

`deepiri-axiom` treats [`exovra-jayden`](https://github.com/exovrix/exovra-jayden) as the upstream source of truth for **org-neutral** skills (precedent: `2d2107a`). Sync rules:

- **Port** only skills with no Exovra/Sovra coupling, and retarget the rest to real Deepiri services (never invent a Deepiri path to satisfy a reference).
- **Skip** anything Exovra-bound: platform internals (`nexus-api`, `cognition*`, `apex-training-ops`, `associate-integration`, `finetune-pipeline`, `integration-probe`, `mcp-tools`, `parasail-streams`, `ollama-models`, `elrot`), org tooling (`platform`, `exovra-dtm`, `submodule-workflow`, `release-train`, `product-design-docs`), hardware (`electrical-engineering`, `pcb-electrical-design`, `firmware-dev-design`, `sovra-*`, `jobs-to-woz`), and Exovra research CSVs (`research`).
- **Skip** anything already covered here, to avoid two drifting copies: `axiom-code-review`, `axiom-debug`, `axiom-observability`, `axiom-incident-response`, `axiom-security-review`, `axiom-adr-writing`, `axiom-api-contract-design`, `axiom-test-plan`, `axiom-tech-debt`, `axiom-dependency-audit`, `axiom-performance-triage`, `axiom-pr-description`, `axiom-secrets-hygiene`, `axiom-onboarding-new-dev`, `axiom-systematic-debugging`, `axiom-changelog-writing`.

| Skill | Invoke for |
|-------|------------|
| pmf-master | Product-market fit via lateral reframes — re-cut the market, exploit the underused asset, build a compounding fit engine (Phase 0–6) |
| validate-idea | Test the idea before building — manual sale, 10 named customers, red/green flags |
| mvp | Discovery, briefs, weekend MVP |
| ship | Weekend scope: cut, manual-first, one outcome |
| processize | Manual process before automation |
| pricing | Initial price and tiers |
| find-community | Where customers already gather |
| marketing-plan | Content-led marketing after fit |
| grow-sustainably | Hire / spend / scale decisions |
| company-values | Culture as decision constraints |
| minimalist-review | Gut-check any plan against lean rules |
| locksmith-genius | "Impossible" blocker — reframe, outsider loop, system fix |
| demo-idea-generator | Novel demo portfolio (25–100 concepts) |
| competitive-analysis | Competitor matrix, pricing bands, gaps |
| business-analyst | BRD, user stories, acceptance criteria, process flows |
| product-roadmap | Now / next / later tied to metrics and owning repo |
| stakeholder-map | RACI |
| requirements-trace | Story → test coverage matrix |
| user-interview | JTBD discovery interview guide |
| docs-writer | READMEs, runbooks, architecture guides |
| find-skills | Discover/install more skills via `npx skills` |
| threat-model | Lightweight STRIDE per service boundary |
| data-quality | Dataset + training-data schema, nulls, leakage, PII |
| agent-watchdog | Audit or fix another agent's work from a transcript/PR/log |
| cross-model-review | Second opinion from a different model before merging risky work |
| efficient-fable / efficient-frontier | Frontier model orchestrates, cheaper subagents do bulk lifting |
| grounded-commit-relay | Multi-agent ideation with trigger-gated push-back and one committed pick |
| plan-arbiter | Pick among competing agent plans |
| plow-ahead | Autonomous progress; state assumptions, don't stop |
| stay-within-limits | Pause near usage caps between waves |
| token-efficiency | Context and token budgeting for long sessions |
| quick-recap | 🟢/🟡/🔴 final status block |
| composition-patterns | React compound components, render props, context |
| react-best-practices | React/Next.js performance patterns |
| web-design-guidelines | UI / a11y / UX audit vs Web Interface Guidelines |
| writing-guidelines | Docs / prose tone audit |
