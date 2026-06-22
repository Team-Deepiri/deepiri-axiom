#!/usr/bin/env python3
"""Generate packaged Deepiri Axiom skills under skills/."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "skills"

SKILLS: list[tuple[str, str, str]] = [
    (
        "deepiri-axiom",
        "Canonical Deepiri systems architect — full org context, AXIOM modes, service boundaries.",
        """Use for **any** Team-Deepiri architecture, cross-repo, or platform-wide question.

## Behavior
- Ground on `docs/DOCUMENTATION_INDEX.md` and `docs/architecture/*` when a clone exists.
- Respect service boundaries: no cross-service DB access; auth before expensive work.
- Cite owning repos; flag doc↔code drift.

## Modes
Announce: SCAN | ARCHITECT | REFACTOR | DEBUG | TEACH | REVIEW.

Run `./setup.sh` to refresh `.axiom/ecosystem.json` with local clones and providers.""",
    ),
    (
        "deepiri-ecosystem",
        "Bootstrap and read the Deepiri ecosystem manifest (.axiom/ecosystem.json).",
        """Triggers: setup, sibling repos, device/GPU, model providers, linking clones.

## Commands
```bash
./setup.sh
python3 setup.py detect --write
python3 setup.py link
python3 setup.py status
```

Prefer **detected local paths** from the manifest over guessing clone locations.""",
    ),
    (
        "deepiri-service-boundaries",
        "Enforce Deepiri microservice ownership and trust boundaries.",
        """Non-negotiable:
- Each service owns its Postgres schema + Prisma migrations.
- Cross-service data via HTTP, queues, or streams — never shared DB reads.
- Gateway + auth validate **before** heavy handlers.
- Route changes to the **owning repo**; state blast radius.""",
    ),
    (
        "deepiri-doc-grounding",
        "Navigate Deepiri docs before sweeping architectural claims.",
        """Read order when inside a clone:
1. `docs/DOCUMENTATION_INDEX.md`
2. `docs/architecture/SYSTEM_ARCHITECTURE.md`
3. `docs/architecture/SERVICES_OVERVIEW.md`
4. Root `README.md`, `.env` / compose for ports

If no clone: use org repo map and name exact repo to open.""",
    ),
    (
        "deepiri-gateway-auth",
        "API gateway and auth-service trust boundary patterns.",
        """Repos: `deepiri-api-gateway` (~5100), `deepiri-auth-service`.

- Gateway is the edge; auth runs before expensive downstream work.
- Never bypass gateway auth for “convenience” in internal calls from UI.
- Verify ports in compose / `.env` — do not invent defaults.""",
    ),
    (
        "deepiri-api-gateway",
        "Route design, proxy rules, and edge concerns for deepiri-api-gateway.",
        """Owns: routing to core-api, auth, external-bridge, language-intelligence.

Check: middleware order, rate limits, request ID propagation, CORS, health checks.
Document any new upstream in gateway config + `docs/architecture/`.""",
    ),
    (
        "deepiri-core-api",
        "Core application API — Express, Prisma, PostgreSQL ownership.",
        """Repo: `deepiri-core-api`.

Migrations live **here only** for core domain tables.
Cross-service features: call other services over HTTP, don't reach into their DB.""",
    ),
    (
        "deepiri-external-bridge",
        "External SaaS integrations — Notion, Trello, GitHub webhooks.",
        """Repo: `deepiri-external-bridge-service`.

Webhook ingress lands here — verify signature/auth paths.
Map inbound events to internal APIs; no direct DB writes to other services' schemas.""",
    ),
    (
        "deepiri-language-intelligence",
        "Linguistic data processing runtime service.",
        """Repo: `deepiri-language-intelligence-service`.

Fronts LI workloads for the platform. Check API contracts with gateway and core-api.""",
    ),
    (
        "deepiri-web-frontend",
        "React + Vite centralized frontend hub (~5173).",
        """Repo: `deepiri-web-frontend`.

Calls gateway (~5100), not core services directly for authenticated flows.
Check env for `VITE_*` API URLs; align with compose port map.""",
    ),
    (
        "diri-cyrex",
        "Cyrex agentic runtime — FastAPI ~8000.",
        """Repo: `diri-cyrex`.

Agent loops, tool calls, runtime orchestration. Uses `deepiri-modelkit`.
Pair with `diri-agent-guardrails` and `diri-agent-toolbox` for production agents.""",
    ),
    (
        "diri-persola",
        "Persola personality and emotion fine-tuning ~8010.",
        """Repo: `diri-persola`.

Human-like personality/emotion layers for agents. Training vs inference paths differ —
confirm dataset and eval harness (`deepiri-tombstone`) before release advice.""",
    ),
    (
        "diri-helox",
        "Helox model fine-tuning and versioning framework.",
        """Repo: `diri-helox`.

Model registry, training pipelines, version promotion. Shares `deepiri-modelkit` with Cyrex.""",
    ),
    (
        "deepiri-modelkit",
        "Shared Python utilities between Cyrex and Helox.",
        """Repo: `deepiri-modelkit`.

Breaking changes require coordinated bumps in Cyrex + Helox; use `deepiri-cascade`.""",
    ),
    (
        "deepiri-prismpipe",
        "Capability-routed API pipeline — model/service routing.",
        """Repo: `deepiri-prismpipe`.

Routes requests by capability to the right backend (Cyrex, Ollama, cloud APIs).
Document routing tables and fallback behavior.""",
    ),
    (
        "deepiri-synapse",
        "Synapse sidecar runtime extracted from platform.",
        """Repo: `deepiri-synapse`.

Streaming / sidecar patterns. Pairs with `deepiri-sugar-glider` (Go transport).""",
    ),
    (
        "deepiri-sugar-glider",
        "Go sidecar extension for Synapse — Redis streams, gRPC.",
        """Repo: `deepiri-sugar-glider`.

Transport layer for Synapse. Check proto contracts and redis stream naming.""",
    ),
    (
        "deepiri-training-orchestrator",
        "Training job orchestration across Deepiri ML repos.",
        """Repo: `deepiri-training-orchestrator`.

Schedules and tracks training jobs; integrate with Helox versioning and dataset-processor.""",
    ),
    (
        "deepiri-dataset-processor",
        "Dataset ingestion and preparation pipelines.",
        """Repo: `deepiri-dataset-processor`.

Upstream of training — validate schema, PII policy, and output locations before Helox jobs.""",
    ),
    (
        "diri-agent-guardrails",
        "Output guardrails for agentic systems.",
        """Repo: `diri-agent-guardrails`.

Apply on Cyrex agent outputs; define policies per deployment, not per prompt hack.""",
    ),
    (
        "diri-agent-toolbox",
        "Agentic tools library for Cyrex and friends.",
        """Repo: `diri-agent-toolbox`.

New tools: explicit schemas, idempotency, timeout budgets, error surfaces for the runtime.""",
    ),
    (
        "deepiri-ollama-local",
        "Local LLM serving with Ollama and deepiri-ollama-utils.",
        """Repos: `deepiri-ollama-utils`, local Ollama on :11434.

Check `./setup.sh` / ecosystem manifest for available models.
Prefer local inference when GPU present; document model tags in compose.""",
    ),
    (
        "deepiri-gpu-zepgpu",
        "GPU utilities and ZepGPU serverless kernel service.",
        """Repos: `deepiri-gpu-utils`, `deepiri-zepgpu`.

Kernel-as-a-service patterns. Verify CUDA visibility (esp. WSL) before recommending GPU paths.""",
    ),
    (
        "deepiri-vizult",
        "Architecture graph and inter-service communication mapping.",
        """Repo: `deepiri-vizult` (Ruby).

```bash
bundle exec ruby exe/vizult scan /path/to/deepiri-platform --siblings
```

Use `vizult-output/graph.json` for evidence-backed architecture answers.""",
    ),
    (
        "deepiri-cascade",
        "Cross-repository dependency version alignment.",
        """Repo: `deepiri-cascade`.

When bumping shared libs (`deepiri-modelkit`, `deepiri-shared-utils`), run cascade alignment across dependents.""",
    ),
    (
        "deepiri-conduit",
        "Service port conflict resolver (Rust).",
        """Repo: `deepiri-conduit`.

Use when local compose port collisions block dev — Conduit assigns/coordinates ports.""",
    ),
    (
        "deepiri-wooven",
        "Credentials manager and git SSH/HTTPS transport helper.",
        """Repo: `deepiri-wooven`.

PAT in OS keyring, `git-credential-wooven`, clone transport auto-pick.
Never commit tokens — Wooven manages HTTPS auth.""",
    ),
    (
        "deepiri-memorymesh",
        "Cross-provider LLM context and memory bridge.",
        """Repo: `deepiri-memorymesh`.

Bridge context between providers/sessions; respect privacy and retention policies.""",
    ),
    (
        "deepiri-pkg-version-manager",
        "Dependency graph, tags, and version management.",
        """Repo: `deepiri-pkg-version-manager`.

Pair with `deepiri-cascade` for org-wide version bumps and release coordination.""",
    ),
    (
        "axiom-scan",
        "AXIOM SCAN mode — full codebase cartography and diagnosis.",
        """Trigger: repo audit, onboarding, large unfamiliar tree.

Output structure:
## CODEBASE DIAGNOSIS
### System Overview / Architecture Pattern / Technology Stack
### Critical Findings [CRITICAL|HIGH|MEDIUM|LOW]
### Recommended Actions / Risk Map

Do not skip to fixes before coverage.""",
    ),
    (
        "axiom-architect",
        "AXIOM ARCHITECT mode — new system design with explicit tradeoffs.",
        """Deliver: requirements, diagram-level design, contracts, failure modes, rollout plan.
Every recommendation states what you give up by not choosing alternatives.""",
    ),
    (
        "axiom-debug",
        "AXIOM DEBUG mode — root cause, not symptom chasing.",
        """Loop: symptoms → ranked hypotheses → falsify → root cause → fix + prevention.
State confidence: CERTAIN | HIGH | MODERATE | HYPOTHESIS | UNKNOWN.""",
    ),
    (
        "axiom-refactor",
        "AXIOM REFACTOR mode — migration-safe structural improvement.",
        """Order: delete → simplify → move → refactor → replace → add.
Include current vs target, migration steps, and tests that prove behavior preserved.""",
    ),
    (
        "axiom-review",
        "AXIOM REVIEW mode — PR/code review with blocking vs suggestion.",
        """Sections: Blocking / Important / Suggestion / Praise (real praise only).
Check service boundaries, auth order, migrations ownership, and test gaps.""",
    ),
    (
        "deepiri-compose-dev",
        "Local Docker Compose dev loop for Deepiri platform.",
        """Start from `deepiri-platform` README and `team_dev_environments/`.
Confirm Postgres, Redis, Kafka, service ports in compose before debugging “connection refused”.""",
    ),
    (
        "deepiri-skaffold-k8s",
        "Skaffold and Kubernetes deployment for Deepiri services.",
        """Check Skaffold manifests, K8s overlays, and secrets management.
Local compose ≠ cluster — verify env-specific config.""",
    ),
    (
        "deepiri-cross-repo",
        "Multi-repo changes, submodules, and coordinated PRs.",
        """Read `BRANCH_PROTECTION.md`, `team_submodule_commands/` when present.
Use `deepiri-sorge` patterns for automated PR workflows where applicable.""",
    ),
    (
        "deepiri-aarflingo",
        "Aarflingo multimodal canine intent forecasting.",
        """Repo: `deepiri-aarflingo`.

`./setup.sh --run` for runtime + studio. Python services + optional GPU for vision/audio.""",
    ),
    (
        "deepiri-polylogue",
        "Filesystem-first shared LLM streaming journal (SJN).",
        """Repo: `deepiri-polylogue`.

Multi-agent coordination via shared journal files — not ad-hoc copy-paste between chats.""",
    ),
    (
        "deepiri-sorge",
        "Autonomous GitHub PR bot workflows.",
        """Repo: `deepiri-sorge`.

Bot-driven PR automation — align with branch protection and team review policy.""",
    ),
    (
        "deepiri-boardman",
        "AI Kanban board assistant.",
        """Repo: `deepiri-boardman`.

Task board intelligence — keep integrations scoped; don't leak platform DB across services.""",
    ),
    (
        "deepiri-huddle",
        "Weekly meeting agenda AI agent.",
        """Repo: `deepiri-huddle`.

Agenda generation from team signals — external calendar/doc APIs via bridge patterns.""",
    ),
    (
        "deepiri-tombstone",
        "Post-training evaluation harness.",
        """Repo: `deepiri-tombstone`.

Eval before promoting Helox/Persola model versions — tie metrics to release gates.""",
    ),
    (
        "deepiri-emotion",
        "Desktop IDE and coding-assistant TUI.",
        """Repo: `deepiri-emotion`.

Rust TUI assistant — separate from web frontend; local-first UX patterns.""",
    ),
    (
        "deepiri-renderflow",
        "AI-native animation and post-production studio.",
        """Repo: `deepiri-renderflow-studio`.

GPU-heavy creative pipeline — check zepgpu/gpu-utils for compute paths.""",
    ),
    (
        "deepiri-egottol",
        "SPICE, VHDL, GPU avionics simulation lab.",
        """Repo: `deepiri-egottol`.

C++/GPU analysis — distinct from product microservices; cite egottol docs for protocol sim.""",
    ),
]


def write_skill(name: str, description: str, body: str) -> None:
    dest = ROOT / name
    dest.mkdir(parents=True, exist_ok=True)
    content = f"""---
name: {name}
description: {description}
---

# {name.replace("-", " ").title()}

{body.strip()}
"""
    (dest / "SKILL.md").write_text(content, encoding="utf-8")


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    for name, desc, body in SKILLS:
        write_skill(name, desc, body)
    print(f"Wrote {len(SKILLS)} skills to {ROOT}")


if __name__ == "__main__":
    main()
