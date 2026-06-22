"""Detect local Deepiri repo clones — multi-root search + git remote matching."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from ecosystem.catalog import RepoEntry, get_catalog_by_name, is_deepiri_repo_name

DEFAULT_ORG = "Team-Deepiri"

_ORG_REMOTE_RE = re.compile(
    rf"github\.com[:/](?P<org>[^/]+)/(?P<repo>[^/.\s]+?)(?:\.git)?$",
    re.IGNORECASE,
)


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
    discovery: str = ""

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
            "discovery": self.discovery,
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


def repo_name_from_remote(url: str, org: str = DEFAULT_ORG) -> str | None:
    """Resolve canonical repo name from origin URL (folder name may differ)."""
    if not url:
        return None
    m = _ORG_REMOTE_RE.search(url.strip())
    if m and m.group("org").lower() == org.lower():
        return m.group("repo")
    return None


def _clone_search_roots(anchor: Path) -> list[tuple[Path, str]]:
    """Return (directory, label) roots to scan for git clones."""
    anchor = anchor.resolve()
    roots: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    home = Path.home()

    def add(path: Path, label: str) -> None:
        p = path.expanduser().resolve()
        if not p.is_dir():
            return
        if p in seen:
            return
        # Avoid scanning system temp roots (permission noise, huge dirs).
        if p in (Path("/"), Path("/tmp")) or p.name in ("proc", "sys", "dev"):
            return
        seen.add(p)
        roots.append((p, label))

    add(anchor, "anchor")
    for i, parent in enumerate(anchor.parents):
        if i >= 4:
            break
        if parent == Path("/"):
            break
        if parent == Path("/tmp"):
            continue
        if parent not in anchor.parents and parent != home and home not in parent.parents:
            # Skip unrelated system paths above pytest temp dirs.
            if str(parent).startswith("/tmp"):
                continue
        add(parent, f"parent:{i}")

    env_roots = os.environ.get("DEEPIRI_CLONE_ROOTS", "")
    env_paths = [Path(p.strip()).expanduser() for p in env_roots.split(os.pathsep) if p.strip()]

    for part in env_paths:
        add(part, "env:DEEPIRI_CLONE_ROOTS")

    if not env_paths:
        for candidate, label in (
            (home / "Documents" / "Deepiri", "~/Documents/Deepiri"),
            (home / "Documents", "~/Documents"),
            (home / "src", "~/src"),
            (home / "projects", "~/projects"),
            (home / "code", "~/code"),
            (home / "dev", "~/dev"),
            (home / "git", "~/git"),
            (home / "repos", "~/repos"),
        ):
            add(candidate, label)

    return roots


def _inspect_repo_dir(
    path: Path,
    catalog: dict[str, RepoEntry],
    *,
    discovery: str,
    org: str = DEFAULT_ORG,
) -> LocalRepo | None:
    if not path.is_dir():
        return None

    try:
        is_git = (path / ".git").exists()
    except OSError:
        is_git = False

    remote = _git_remote(path) if is_git else ""
    name = repo_name_from_remote(remote, org=org)
    if not name and is_deepiri_repo_name(path.name):
        name = path.name
    if not name:
        return None

    entry = catalog.get(name)
    return LocalRepo(
        name=name,
        path=str(path.resolve()),
        category=entry.category if entry else "unknown",
        role=entry.role if entry else "",
        stack=entry.stack if entry else "",
        has_git=(path / ".git").exists(),
        remote_url=remote,
        default_branch=_git_default_branch(path) if remote else "",
        has_setup_sh=(path / "setup.sh").is_file(),
        has_pyproject=(path / "pyproject.toml").is_file(),
        has_package_json=(path / "package.json").is_file(),
        discovery=discovery,
    )


def _scan_root(root: Path, catalog: dict[str, RepoEntry], label: str) -> list[LocalRepo]:
    found: list[LocalRepo] = []
    try:
        children = sorted(root.iterdir())
    except OSError:
        return found

    for child in children:
        if not child.is_dir() or child.name.startswith("."):
            continue
        try:
            repo = _inspect_repo_dir(child, catalog, discovery=label)
        except OSError:
            continue
        if repo:
            found.append(repo)
    return found


def discover_local_repos(anchor: Path, *, catalog: dict[str, RepoEntry] | None = None) -> list[LocalRepo]:
    """Find Team-Deepiri clones across common roots; match by remote URL or name prefix."""
    anchor = anchor.resolve()
    if catalog is None:
        catalog = get_catalog_by_name(anchor)

    seen_paths: set[str] = set()
    found: list[LocalRepo] = []

    def add_repo(repo: LocalRepo | None) -> None:
        if repo and repo.path not in seen_paths:
            seen_paths.add(repo.path)
            found.append(repo)

    for root, label in _clone_search_roots(anchor):
        add_repo(_inspect_repo_dir(root, catalog, discovery=label))
        for repo in _scan_root(root, catalog, label):
            add_repo(repo)

    found.sort(key=lambda r: r.name)
    return found


def scan_sibling_repos(anchor: Path, *, max_depth: int = 2) -> list[LocalRepo]:
    """Backward-compatible alias — now uses multi-root discovery."""
    _ = max_depth
    return discover_local_repos(anchor)


def repo_links(repos: list[LocalRepo]) -> list[dict[str, str]]:
    """Infer links from local manifests (delegates to link_inference)."""
    from ecosystem.link_inference import infer_repo_links

    return infer_repo_links(repos)


def repos_markdown(repos: list[LocalRepo]) -> str:
    """Markdown table for prompt injection."""
    if not repos:
        return (
            "_No local Team-Deepiri clones detected. Set `DEEPIRI_CLONE_ROOTS` "
            "(pathsep-separated) or clone repos — matching works via `git remote` too._\n"
        )
    lines = [
        "## Local ecosystem (detected clones)",
        "",
        "| repo | path | stack | discovery |",
        "|------|------|-------|-----------|",
    ]
    for r in repos:
        lines.append(
            f"| `{r.name}` | `{r.path}` | {r.stack or '—'} | {r.discovery or '—'} |"
        )
    lines.append("")
    return "\n".join(lines)
