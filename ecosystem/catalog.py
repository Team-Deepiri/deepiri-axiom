"""Canonical Team-Deepiri repo catalog for linking and prompts."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RepoEntry:
    name: str
    category: str
    role: str
    stack: str = ""
    default_port: int | None = None


# Authoritative org catalog — used for sibling detection and prompt injection.
DEEPIRI_REPO_CATALOG: tuple[RepoEntry, ...] = (
    # Platform & runtime — Node / TypeScript
    RepoEntry("deepiri-platform", "platform", "Main monorepo; docs, compose, team_dev_environments", "node"),
    RepoEntry("deepiri-api-gateway", "platform", "Edge gateway — trust boundary", "node", 5100),
    RepoEntry("deepiri-core-api", "platform", "Core application API (Express + Prisma)", "node"),
    RepoEntry("deepiri-auth-service", "platform", "Authentication / session / token service", "node"),
    RepoEntry(
        "deepiri-external-bridge-service",
        "platform",
        "External SaaS integrations (Notion, Trello, GitHub)",
        "node",
    ),
    RepoEntry(
        "deepiri-language-intelligence-service",
        "platform",
        "Runtime linguistic-data processing",
        "node",
    ),
    RepoEntry("deepiri-web-frontend", "platform", "Centralized React + Vite frontend hub", "node", 5173),
    RepoEntry("deepiri-landing", "platform", "Marketing / landing page", "node"),
    RepoEntry("deepiri-shared-utils", "platform", "Shared TS utilities across Node services", "node"),
    # AI runtime — Python
    RepoEntry("diri-cyrex", "ai-runtime", "Cyrex agentic runtime framework", "python", 8000),
    RepoEntry("diri-persola", "ai-runtime", "Personality/emotion fine-tuning framework", "python", 8010),
    RepoEntry("diri-helox", "ai-runtime", "Model fine-tuning and versioning", "python"),
    RepoEntry("deepiri-modelkit", "ai-runtime", "Shared Python lib between Cyrex and Helox", "python"),
    RepoEntry("deepiri-prismpipe", "ai-runtime", "Capability-routed API pipeline", "python"),
    RepoEntry("deepiri-synapse", "ai-runtime", "Synapse sidecar runtime", "python"),
    RepoEntry("deepiri-training-orchestrator", "ai-runtime", "Training-job orchestration", "python"),
    RepoEntry("deepiri-dataset-processor", "ai-runtime", "Dataset ingestion / preparation", "python"),
    RepoEntry("diri-agent-testing-utils", "ai-runtime", "Agent evaluation test utilities", "python"),
    RepoEntry("diri-agent-guardrails", "ai-runtime", "Guardrail framework for agent outputs", "python"),
    RepoEntry("diri-agent-toolbox", "ai-runtime", "Agentic tools library", "python"),
    RepoEntry("deepiri-ollama-utils", "ai-runtime", "Ollama helpers for local LLM serving", "python"),
    RepoEntry("deepiri-aarflingo", "ai-runtime", "Proactive canine intent forecasting (multimodal)", "python"),
    RepoEntry("deepiri-tombstone", "ai-runtime", "Post-training evaluation harness", "python"),
    # Infrastructure & glue
    RepoEntry("deepiri-sugar-glider", "infra", "Go sidecar extension for Synapse", "go"),
    RepoEntry("deepiri-conduit", "infra", "Service port-conflict resolver", "rust"),
    RepoEntry("deepiri-cascade", "infra", "Cross-repo dependency version alignment", "python"),
    RepoEntry("deepiri-pkg-version-manager", "infra", "Dependency graph + tag + version management", "python"),
    RepoEntry("deepiri-vizult", "infra", "Inter-service architecture mapping toolkit", "ruby"),
    RepoEntry("deepiri-gpu-utils", "infra", "GPU utility library", "python"),
    RepoEntry("deepiri-zepgpu", "infra", "Serverless GPU / kernel-as-a-service", "python"),
    RepoEntry("deepiri-axiom", "infra", "AI systems architect subagent (this repo)", "python"),
    RepoEntry("deepiri-wooven", "infra", "Credentials manager + git transport helper", "python"),
    RepoEntry("deepiri-memorymesh", "infra", "LLM cross-provider context / memory bridge", "python"),
    RepoEntry("deepiri-logger", "infra", "Shared logging utilities", "python"),
    # Bots & DX
    RepoEntry("deepiri-sorge", "dx", "Autonomous GitHub PR bot", "python"),
    RepoEntry("deepiri-norozo", "dx", "Discord / GitHub communications bot", "python"),
    RepoEntry("deepiri-demo", "dx", "CI/CD and GitHub Actions testing repo", "node"),
    RepoEntry("deepiri-boardman", "dx", "AI Kanban board assistant", "python"),
    RepoEntry("deepiri-huddle", "dx", "AI agent for weekly meeting agendas", "python"),
    RepoEntry("deepiri-polylogue", "dx", "Filesystem-first shared LLM streaming journal", "python"),
    # Creative / side projects
    RepoEntry("deepiri-emotion", "creative", "Desktop IDE and coding-assistant TUI", "rust"),
    RepoEntry("deepiri-lyback", "creative", "Interactive embeddable mini-game backgrounds", "node"),
    RepoEntry("deepiri-voxier", "creative", "Godot Fox Rocket game", "godot"),
    RepoEntry("deepiri-egottol", "creative", "SPICE/VHDL/GPU avionics simulation lab", "cpp"),
    RepoEntry("deepiri-renderflow-studio", "creative", "AI-native animation and post-production", "python"),
    RepoEntry("deepiri-calliope", "creative", "AI music studio", "python"),
    RepoEntry("deepiri-mistspire", "creative", "PCVR world", "unity"),
    RepoEntry("deepiri-metal-omelette", "creative", "Binary VM runtime and instruction set", "rust"),
    RepoEntry("deepiri-mudspeed", "creative", "GPU emulator via Neural ODE models", "python"),
    RepoEntry("deepiri-uqe", "creative", "Universal quantum engine", "python"),
    RepoEntry("deepiri-suite", "creative", "Product suite umbrella", "mixed"),
)

CATALOG_BY_NAME: dict[str, RepoEntry] = {e.name: e for e in DEEPIRI_REPO_CATALOG}

DEEPIRI_REPO_PREFIXES = ("deepiri-", "diri-")


def is_deepiri_repo_name(name: str) -> bool:
    return any(name.startswith(p) for p in DEEPIRI_REPO_PREFIXES)
