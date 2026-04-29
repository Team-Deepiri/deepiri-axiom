"""Install-time snapshot of a target repo layout (npm workspaces, services, submodules).

Keeps prompts data-driven: generated when ``setup.py install`` runs, not hand-edited tables.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

_MAX_LIST = 60

_GLOBAL_SNAPSHOT_OMIT = (
    "\n## Target repo snapshot (user-level install)\n\n"
    "Omitted: embedding a per-repo tree would go stale in other workspaces. "
    "For a fresh layout, run the installer in that repository, for example: "
    "`python3 <path-to-deepiri-axiom>/setup.py subagent` from the repo root "
    "(or `python3 <path-to-deepiri-axiom>/setup.py install --target <repo> --tools cursor`).\n\n"
    "This file still includes **AXIOM core** and **Deepiri context** in any folder.\n"
)


def _read_package_json_name(pkg_json: Path) -> str | None:
    try:
        data = json.loads(pkg_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return None
    name = data.get("name")
    return name if isinstance(name, str) and name.strip() else None


def _workspace_patterns(root: Path) -> list[str]:
    pkg = root / "package.json"
    if not pkg.is_file():
        return []
    try:
        data = json.loads(pkg.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return []
    ws = data.get("workspaces")
    if isinstance(ws, list):
        return [str(x).strip() for x in ws if isinstance(x, str) and str(x).strip()]
    if isinstance(ws, dict):
        pkgs = ws.get("packages")
        if isinstance(pkgs, list):
            return [str(x).strip() for x in pkgs if isinstance(x, str) and str(x).strip()]
    return []


def _dirs_for_workspace_pattern(root: Path, pattern: str) -> list[Path]:
    pattern = pattern.replace("\\", "/").strip()
    if not pattern:
        return []
    if any(c in pattern for c in "*?[]"):
        return sorted(p for p in root.glob(pattern) if p.is_dir())
    p = root / pattern
    return [p] if p.is_dir() else []


def _parse_gitmodules(path: Path) -> list[tuple[str, str]]:
    """Return (submodule name, relative path) from ``.gitmodules``."""
    if not path.is_file():
        return []
    current: str | None = None
    out: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        m = re.match(r'^\[submodule\s+"([^"]+)"\s*\]', line)
        if m:
            current = m.group(1)
            continue
        if current and line.startswith("path ="):
            rel = line.split("=", 1)[1].strip()
            out.append((current, rel))
            current = None
    return out


def _markdown_escape_cell(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ")


def build_target_cartography(target: Path) -> str:
    """Return markdown: install-time layout snapshot for ``target`` (usually ``--install`` root)."""
    lines: list[str] = [
        "## Target repo snapshot (install-time)",
        "",
        "*Generated when `deepiri-axiom` was installed into this tree. Re-run "
        "`python3 path/to/deepiri-axiom/setup.py install --target .` to refresh.*",
        "",
    ]
    if not target.is_dir():
        lines.append(f"_Not a directory: `{target}`._")
        return "\n".join(lines)

    root = target.resolve()
    lines.append(f"- **Root:** `{root}`")

    doc_index = root / "docs" / "DOCUMENTATION_INDEX.md"
    if doc_index.is_file():
        lines.append("- **Docs index:** `docs/DOCUMENTATION_INDEX.md` (use as navigation hub)")
    bp = root / "BRANCH_PROTECTION.md"
    if bp.is_file():
        lines.append("- **Branch policy:** `BRANCH_PROTECTION.md` (read before merge/release advice)")

    for hint in (
        "team_submodule_commands",
        "team_dev_environments",
    ):
        p = root / hint
        if p.is_dir():
            lines.append(f"- **Team workflows:** `{hint}/`")

    # Workspaces → packages
    patterns = _workspace_patterns(root)
    workspace_dirs: list[Path] = []
    seen: set[Path] = set()
    for pat in patterns:
        for d in _dirs_for_workspace_pattern(root, pat):
            rp = d.resolve()
            if rp not in seen:
                seen.add(rp)
                workspace_dirs.append(d)
    workspace_dirs.sort(key=lambda p: str(p))

    if patterns:
        lines.append("")
        lines.append("### npm workspaces (from root `package.json`)")
        lines.append("")
        lines.append("| Workspace pattern | Resolved package dirs |")
        lines.append("|-------------------|------------------------|")
        for pat in patterns:
            dirs = _dirs_for_workspace_pattern(root, pat)
            if len(dirs) > _MAX_LIST:
                shown = dirs[:_MAX_LIST]
                extra = f" … *and {len(dirs) - _MAX_LIST} more*"
            else:
                shown = dirs
                extra = ""
            cell = ", ".join(f"`{d.relative_to(root)}`" for d in shown) + extra
            lines.append(f"| `{_markdown_escape_cell(pat)}` | {cell} |")

    packages: list[tuple[str, str]] = []
    for d in workspace_dirs:
        pj = d / "package.json"
        if not pj.is_file():
            continue
        name = _read_package_json_name(pj) or d.name
        rel = str(d.relative_to(root))
        packages.append((name, rel))
    packages.sort(key=lambda x: x[1])

    if packages:
        lines.append("")
        lines.append("### Workspace packages (name → path)")
        lines.append("")
        lines.append("| name | path |")
        lines.append("|------|------|")
        for name, rel in packages[:_MAX_LIST]:
            lines.append(f"| `{_markdown_escape_cell(name)}` | `{_markdown_escape_cell(rel)}` |")
        if len(packages) > _MAX_LIST:
            lines.append(f"| … | *{len(packages) - _MAX_LIST} more* |")

    # Submodules
    gm = root / ".gitmodules"
    subs = _parse_gitmodules(gm)
    if subs:
        lines.append("")
        lines.append("### Git submodules (from `.gitmodules`)")
        lines.append("")
        lines.append("| submodule | path |")
        lines.append("|-----------|------|")
        for name, path in subs[:_MAX_LIST]:
            lines.append(
                f"| `{_markdown_escape_cell(name)}` | `{_markdown_escape_cell(path)}` |"
            )
        if len(subs) > _MAX_LIST:
            lines.append(f"| … | *{len(subs) - _MAX_LIST} more* |")
        lines.append("")
        lines.append(
            "*If the task touches shared code or release flow, align with submodule pointers "
            "(`git submodule status`) and team scripts under `team_submodule_commands/` when present.*"
        )

    if not patterns and not subs:
        lines.append("")
        lines.append(
            "_No root `package.json` workspaces and no `.gitmodules` detected — "
            "use this repo's `README.md` and `docs/` for layout._"
        )

    return "\n".join(lines) + "\n"


def global_user_cartography() -> str:
    """Text for `TARGET_REPO_CARTOGRAPHY` in user-level (``~/.cursor/agents/``) installs."""
    return _GLOBAL_SNAPSHOT_OMIT
