"""Persisted ecosystem manifest (.axiom/ecosystem.json)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


MANIFEST_VERSION = 1
MANIFEST_DIR = ".axiom"
MANIFEST_FILE = "ecosystem.json"


@dataclass
class EcosystemManifest:
    version: int = MANIFEST_VERSION
    generated_at: str = ""
    device: dict = field(default_factory=dict)
    providers: list[dict] = field(default_factory=list)
    apps: list[dict] = field(default_factory=list)
    repos: list[dict] = field(default_factory=list)
    links: list[dict] = field(default_factory=list)
    recommended_tools: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "version": self.version,
            "generated_at": self.generated_at,
            "device": self.device,
            "providers": self.providers,
            "apps": self.apps,
            "repos": self.repos,
            "links": self.links,
            "recommended_tools": self.recommended_tools,
        }

    @classmethod
    def from_dict(cls, data: dict) -> EcosystemManifest:
        return cls(
            version=int(data.get("version", 1)),
            generated_at=str(data.get("generated_at", "")),
            device=dict(data.get("device", {})),
            providers=list(data.get("providers", [])),
            apps=list(data.get("apps", [])),
            repos=list(data.get("repos", [])),
            links=list(data.get("links", [])),
            recommended_tools=list(data.get("recommended_tools", [])),
        )


def manifest_path(root: Path) -> Path:
    return root / MANIFEST_DIR / MANIFEST_FILE


def load_manifest(root: Path) -> EcosystemManifest | None:
    path = manifest_path(root)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return EcosystemManifest.from_dict(data)
    except (OSError, json.JSONDecodeError):
        pass
    return None


def save_manifest(root: Path, manifest: EcosystemManifest) -> Path:
    path = manifest_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    manifest.generated_at = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(manifest.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def manifest_markdown(manifest: EcosystemManifest) -> str:
    """Compact markdown summary for prompt injection."""
    lines = [
        "## Ecosystem manifest (auto-detected)",
        "",
        f"- **Generated:** {manifest.generated_at or 'unknown'}",
    ]
    dev = manifest.device
    if dev:
        gpu = "yes" if dev.get("has_nvidia_gpu") else "no"
        lines.append(
            f"- **Device:** {dev.get('os_name', '?')} / {dev.get('arch', '?')} "
            f"(WSL={dev.get('is_wsl')}, GPU={gpu}, CPUs={dev.get('cpu_count', '?')})"
        )
    avail_providers = [p["name"] for p in manifest.providers if p.get("available")]
    if avail_providers:
        lines.append(f"- **Model providers:** {', '.join(avail_providers)}")
    local_repos = [r["name"] for r in manifest.repos]
    if local_repos:
        lines.append(f"- **Local clones:** {', '.join(local_repos)}")
    if manifest.links:
        lines.append(f"- **Inferred links:** {len(manifest.links)} edge(s)")
    if manifest.recommended_tools:
        lines.append(f"- **Recommended axiom tools:** {', '.join(manifest.recommended_tools)}")
    lines.append("")
    lines.append(
        "_Refresh with `./setup.sh` or `python3 setup.py detect --write`._"
    )
    lines.append("")
    return "\n".join(lines)
