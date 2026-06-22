"""Detect local Deepiri repo clones and sibling relationships."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from ecosystem.catalog import CATALOG_BY_NAME, DEEPIRI_REPO_PREFIXES, is_deepiri_repo_name


@dataclass
class LocalRepo:
    name: str
    path: str
    category: str = ""
    role: str = ""
    stack: str = ""
    has_git: bool = False
    remote_url: str = ""
    default_branch: str = ""
    has_setup_sh: bool = False
    has_pyproject: bool = False
    has_package_json: bool = False

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "category": self.category,
            "role": self.role,
            "stack": self.stack,
            "has_git": self.has_git,
            "remote_url": self.remote_url,
            "default_branch": self.default_branch,
            "has_setup_sh": self.has_setup_sh,
            "has_pyproject": self.has_pyproject,
            "has_package_json": self.has_package_json,
        }


def _git_remote(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _git_default_branch(path: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "-C", str(path), "symbolic-ref", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        return out.stdout.strip() if out.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _inspect_repo_dir(path: Path) -> LocalRepo | None:
    if not path.is_dir():
        return None
    name = path.name
    if not is_deepiri_repo_name(name):
        return None
    entry = CATALOG_BY_NAME.get(name)
    return LocalRepo(
        name=name,
        path=str(path.resolve()),
        category=entry.category if entry else "unknown",
        role=entry.role if entry else "",
        stack=entry.stack if entry else "",
        has_git=(path / ".git").exists(),
        remote_url=_git_remote(path),
        default_branch=_git_default_branch(path),
        has_setup_sh=(path / "setup.sh").is_file(),
        has_pyproject=(path / "pyproject.toml").is_file(),
        has_package_json=(path / "package.json").is_file(),
    )


def scan_sibling_repos(anchor: Path, *, max_depth: int = 2) -> list[LocalRepo]:
    """Find Deepiri clones near ``anchor`` (parent dirs and shallow children)."""
    anchor = anchor.resolve()
    seen: set[str] = set()
    found: list[LocalRepo] = []

    def add(path: Path) -> None:
        repo = _inspect_repo_dir(path)
        if repo and repo.path not in seen:
            seen.add(repo.path)
            found.append(repo)

    add(anchor)
    for parent in list(anchor.parents)[:max_depth]:
        if not parent.is_dir():
            continue
        try:
            for child in sorted(parent.iterdir()):
                if child.is_dir():
                    add(child)
        except OSError:
            continue

    found.sort(key=lambda r: r.name)
    return found


def repo_links(repos: list[LocalRepo]) -> list[dict[str, str]]:
    """Infer simple dependency hints between detected local repos."""
    names = {r.name for r in repos}
    links: list[dict[str, str]] = []
    hints = [
        ("deepiri-web-frontend", "deepiri-api-gateway", "http"),
        ("deepiri-api-gateway", "deepiri-core-api", "http"),
        ("deepiri-api-gateway", "deepiri-auth-service", "http"),
        ("diri-cyrex", "deepiri-modelkit", "import"),
        ("diri-helox", "deepiri-modelkit", "import"),
        ("deepiri-synapse", "deepiri-sugar-glider", "grpc"),
        ("deepiri-platform", "deepiri-synapse", "submodule"),
        ("deepiri-axiom", "deepiri-platform", "prompt-context"),
        ("deepiri-vizult", "deepiri-platform", "scan"),
        ("deepiri-cascade", "deepiri-pkg-version-manager", "version-align"),
        ("deepiri-prismpipe", "diri-cyrex", "route"),
        ("deepiri-aarflingo", "deepiri-gpu-utils", "optional-gpu"),
    ]
    for src, dst, kind in hints:
        if src in names and dst in names:
            links.append({"from": src, "to": dst, "kind": kind})
    return links


def repos_markdown(repos: list[LocalRepo]) -> str:
    """Markdown table for prompt injection."""
    if not repos:
        return "_No local Deepiri clones detected near this install._\n"
    lines = [
        "## Local ecosystem (detected clones)",
        "",
        "| repo | path | stack | setup.sh |",
        "|------|------|-------|----------|",
    ]
    for r in repos:
        setup = "yes" if r.has_setup_sh else "—"
        lines.append(f"| `{r.name}` | `{r.path}` | {r.stack or '—'} | {setup} |")
    lines.append("")
    return "\n".join(lines)
