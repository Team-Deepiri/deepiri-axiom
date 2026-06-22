"""Canonical Team-Deepiri repo catalog — loaded dynamically from GitHub + cache."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ecosystem.github_catalog import DEFAULT_ORG, catalog_markdown, refresh_org_catalog

DEEPIRI_REPO_PREFIXES = ("deepiri-", "diri-")


@dataclass(frozen=True, slots=True)
class RepoEntry:
    name: str
    category: str
    role: str
    stack: str = ""
    default_port: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> RepoEntry:
        port = data.get("default_port")
        return cls(
            name=str(data["name"]),
            category=str(data.get("category", "unknown")),
            role=str(data.get("role", "")),
            stack=str(data.get("stack") or ""),
            default_port=int(port) if port is not None else None,
        )


def is_deepiri_repo_name(name: str) -> bool:
    return any(name.startswith(p) for p in DEEPIRI_REPO_PREFIXES)


def _dicts_to_entries(rows: list[dict]) -> list[RepoEntry]:
    return [RepoEntry.from_dict(r) for r in rows if r.get("name")]


def get_catalog(
    anchor: Path | None = None,
    *,
    org: str = DEFAULT_ORG,
    force_refresh: bool = False,
) -> tuple[list[RepoEntry], str]:
    """Load org catalog from cache or GitHub API."""
    root = (anchor or Path.cwd()).resolve()
    rows, source = refresh_org_catalog(root, org=org, force=force_refresh)
    return _dicts_to_entries(rows), source


def get_catalog_by_name(anchor: Path | None = None) -> dict[str, RepoEntry]:
    entries, _ = get_catalog(anchor)
    return {e.name: e for e in entries}


def get_catalog_markdown(anchor: Path | None = None) -> str:
    root = (anchor or Path.cwd()).resolve()
    rows, source = refresh_org_catalog(root)
    return catalog_markdown(rows, source=source)
