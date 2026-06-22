"""Fetch and cache Team-Deepiri org catalog from GitHub (no hardcoded repo list)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

DEFAULT_ORG = "Team-Deepiri"
CACHE_FILENAME = "org-catalog.json"
DEFAULT_TTL_SECONDS = 86_400  # 24h

_PLATFORM_HINTS = (
    "api-gateway",
    "core-api",
    "auth-service",
    "web-frontend",
    "landing",
    "bridge",
    "language-intelligence",
    "shared-utils",
    "synapse",
)
_AI_HINTS = (
    "cyrex",
    "persola",
    "helox",
    "modelkit",
    "prismpipe",
    "training",
    "dataset",
    "agent-",
    "ollama",
    "aarflingo",
    "tombstone",
)
_INFRA_HINTS = (
    "vizult",
    "cascade",
    "conduit",
    "wooven",
    "axiom",
    "gpu",
    "zepgpu",
    "sugar-glider",
    "pkg-version",
    "memorymesh",
    "logger",
)
_DX_HINTS = ("sorge", "norozo", "boardman", "huddle", "polylogue", "demo")

_LANG_STACK = {
    "TypeScript": "node",
    "JavaScript": "node",
    "Python": "python",
    "Go": "go",
    "Rust": "rust",
    "Ruby": "ruby",
    "C++": "cpp",
    "C#": "csharp",
    "GDScript": "godot",
}


@dataclass
class OrgCatalogCache:
    org: str
    fetched_at: float
    source: str
    repos: list[dict]

    def to_dict(self) -> dict:
        return {
            "org": self.org,
            "fetched_at": self.fetched_at,
            "source": self.source,
            "repos": self.repos,
        }

    @classmethod
    def from_dict(cls, data: dict) -> OrgCatalogCache:
        return cls(
            org=str(data.get("org", DEFAULT_ORG)),
            fetched_at=float(data.get("fetched_at", 0)),
            source=str(data.get("source", "unknown")),
            repos=list(data.get("repos", [])),
        )


def catalog_cache_path(anchor: Path) -> Path:
    return anchor.resolve() / ".axiom" / CACHE_FILENAME


def _infer_category(name: str, description: str) -> str:
    n = name.lower()
    d = (description or "").lower()
    blob = f"{n} {d}"
    if n == "deepiri-platform" or "monorepo" in d:
        return "platform"
    if n.startswith("diri-") or any(h in blob for h in _AI_HINTS):
        return "ai-runtime"
    if any(h in blob for h in _PLATFORM_HINTS):
        return "platform"
    if any(h in blob for h in _INFRA_HINTS):
        return "infra"
    if any(h in blob for h in _DX_HINTS):
        return "dx"
    if n.startswith("deepiri-") or n.startswith("diri-"):
        return "creative"
    return "unknown"


def _infer_stack(language: str | None, name: str) -> str:
    if language and language in _LANG_STACK:
        return _LANG_STACK[language]
    n = name.lower()
    if "frontend" in n or "landing" in n or "lyback" in n:
        return "node"
    if n.startswith("diri-"):
        return "python"
    if "glider" in n:
        return "go"
    if "conduit" in n or "emotion" in n or "omelette" in n:
        return "rust"
    if "vizult" in n:
        return "ruby"
    if "egottol" in n:
        return "cpp"
    if "voxier" in n:
        return "godot"
    return ""


def _entry_dict(name: str, description: str, language: str | None) -> dict:
    return {
        "name": name,
        "category": _infer_category(name, description),
        "role": description or f"Team-Deepiri/{name}",
        "stack": _infer_stack(language, name),
        "default_port": None,
    }


def _gh_api_repos(org: str) -> list[dict] | None:
    if shutil.which("gh") is None:
        return None
    try:
        out = subprocess.run(
            ["gh", "api", f"orgs/{org}/repos", "--paginate"],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if out.returncode != 0:
            return None
        data = json.loads(out.stdout)
        if isinstance(data, list):
            return data
        return None
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError):
        return None


def _http_api_repos(org: str) -> list[dict] | None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    headers = {
        "User-Agent": "deepiri-axiom/2.0",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    repos: list[dict] = []
    page = 1
    while page <= 10:
        url = f"https://api.github.com/orgs/{org}/repos?per_page=100&page={page}&type=public"
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                batch = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError):
            return repos if repos else None
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos if repos else None


def fetch_org_catalog(org: str = DEFAULT_ORG) -> tuple[list[dict], str]:
    """Fetch org repos from GitHub. Returns (entry dicts, source_label)."""
    raw_list = _gh_api_repos(org)
    source = "gh-api"
    if raw_list is None:
        raw_list = _http_api_repos(org)
        source = "github-rest"
    if not raw_list:
        return [], "unavailable"
    entries = []
    for raw in raw_list:
        name = raw.get("name")
        if not name:
            continue
        desc = str(raw.get("description") or "").strip()
        lang = raw.get("language")
        language = str(lang) if lang else None
        entries.append(_entry_dict(str(name), desc, language))
    entries.sort(key=lambda e: e["name"])
    return entries, source


def load_cached_catalog(anchor: Path) -> OrgCatalogCache | None:
    path = catalog_cache_path(anchor)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return OrgCatalogCache.from_dict(data)
    except (OSError, json.JSONDecodeError):
        pass
    return None


def save_catalog_cache(anchor: Path, cache: OrgCatalogCache) -> Path:
    path = catalog_cache_path(anchor)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache.to_dict(), indent=2) + "\n", encoding="utf-8")
    return path


def refresh_org_catalog(
    anchor: Path,
    *,
    org: str = DEFAULT_ORG,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
    force: bool = False,
) -> tuple[list[dict], str]:
    """Return catalog entry dicts; refresh from GitHub when cache missing or stale."""
    anchor = anchor.resolve()
    cached = load_cached_catalog(anchor)
    now = time.time()
    if cached and not force and (now - cached.fetched_at) < ttl_seconds:
        return cached.repos, f"cache:{cached.source}"

    entries, source = fetch_org_catalog(org)
    if entries:
        save_catalog_cache(
            anchor,
            OrgCatalogCache(org=org, fetched_at=now, source=source, repos=entries),
        )
        return entries, source

    if cached:
        return cached.repos, f"stale-cache:{cached.source}"

    return [], "empty"


def catalog_markdown(entries: list[dict], *, source: str) -> str:
    if not entries:
        return (
            "_Org catalog unavailable — run `./setup.sh` online or set GITHUB_TOKEN. "
            "Local clones are still detected via git remotes._\n"
        )
    lines = [
        f"## Team-Deepiri org catalog ({len(entries)} repos, source: {source})",
        "",
        "| repo | category | stack | role |",
        "|------|----------|-------|------|",
    ]
    for e in entries[:80]:
        role = str(e.get("role", "")).replace("|", "\\|")[:80]
        lines.append(
            f"| `{e['name']}` | {e.get('category', '?')} | {e.get('stack') or '—'} | {role} |"
        )
    if len(entries) > 80:
        lines.append(f"| … | | | *{len(entries) - 80} more in .axiom/org-catalog.json* |")
    lines.append("")
    return "\n".join(lines)
