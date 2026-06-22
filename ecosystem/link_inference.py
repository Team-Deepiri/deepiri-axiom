"""Infer repo-to-repo links from local manifests (not hardcoded hints)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from ecosystem.repos import LocalRepo

DEFAULT_ORG = "Team-Deepiri"

_ORG_REPO_RE = re.compile(
    rf"(?:github\.com[/:]|github:){re.escape(DEFAULT_ORG)}/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?(?:[\"'\s\)\]]|$)",
    re.IGNORECASE,
)

_MANIFEST_NAMES = frozenset(
    {
        "package.json",
        "pyproject.toml",
        "go.mod",
        "Gemfile",
        "compose.yml",
        "compose.yaml",
        "docker-compose.yml",
        "docker-compose.yaml",
        ".gitmodules",
    }
)

_MAX_FILE_BYTES = 256_000
_MAX_WALK_DEPTH = 4


def _read_snippet(path: Path) -> str:
    try:
        if path.stat().st_size > _MAX_FILE_BYTES:
            return path.read_text(encoding="utf-8", errors="replace")[:_MAX_FILE_BYTES]
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _refs_in_text(text: str) -> set[str]:
    return {m.group("repo") for m in _ORG_REPO_RE.finditer(text)}


def _kind_for_file(path: Path) -> str:
    name = path.name
    if name == ".gitmodules":
        return "submodule"
    if name in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"):
        return "compose"
    if name == "go.mod":
        return "go-require"
    if name == "package.json":
        return "npm-dep"
    if name == "pyproject.toml":
        return "python-dep"
    return "reference"


def _manifest_files(repo_root: Path) -> list[Path]:
    found: list[Path] = []
    root = repo_root.resolve()
    if not root.is_dir():
        return found

    def walk(dir_path: Path, depth: int) -> None:
        if depth > _MAX_WALK_DEPTH:
            return
        try:
            entries = sorted(dir_path.iterdir())
        except OSError:
            return
        for entry in entries:
            if entry.name in (".git", "node_modules", ".venv", "vendor", "dist", "build"):
                continue
            if entry.is_file() and entry.name in _MANIFEST_NAMES:
                found.append(entry)
            elif entry.is_dir() and depth < _MAX_WALK_DEPTH:
                walk(entry, depth + 1)

    for name in _MANIFEST_NAMES:
        p = root / name
        if p.is_file():
            found.append(p)
    walk(root, 0)
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in found:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            unique.append(p)
    return unique


def infer_repo_links(repos: list[LocalRepo]) -> list[dict[str, str]]:
    """Infer edges between local repos by scanning manifests for Team-Deepiri references."""
    names = {r.name for r in repos}
    links: list[dict[str, str]] = []
    seen_edges: set[tuple[str, str, str, str]] = set()

    for repo in repos:
        root = Path(repo.path)
        for manifest in _manifest_files(root):
            text = _read_snippet(manifest)
            refs = _refs_in_text(text)
            if manifest.name == "package.json":
                try:
                    data = json.loads(text)
                    if isinstance(data, dict):
                        for key in ("dependencies", "devDependencies", "peerDependencies"):
                            block = data.get(key)
                            if isinstance(block, dict):
                                for val in block.values():
                                    if isinstance(val, str):
                                        refs |= _refs_in_text(val)
                except json.JSONDecodeError:
                    pass
            kind = _kind_for_file(manifest)
            try:
                evidence = str(manifest.relative_to(root))
            except ValueError:
                evidence = manifest.name
            for target in sorted(refs):
                if target == repo.name or target not in names:
                    continue
                key = (repo.name, target, kind, evidence)
                if key in seen_edges:
                    continue
                seen_edges.add(key)
                links.append(
                    {"from": repo.name, "to": target, "kind": kind, "evidence": evidence}
                )

    links.sort(key=lambda e: (e["from"], e["to"], e["kind"]))
    return links
