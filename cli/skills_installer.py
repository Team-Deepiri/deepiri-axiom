"""Install packaged Deepiri Axiom skills into Cursor and Claude skill directories."""

from __future__ import annotations

import re
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"
_SKILL_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}$")


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _render_template(template_body: str, mapping: dict[str, str]) -> str:
    from cli.installer import render_template

    return render_template(template_body, mapping)


def list_skill_dirs() -> list[tuple[str, Path]]:
    """Return sorted (skill_name, skill_dir) for every installable skill."""
    if not SKILLS_ROOT.is_dir():
        return []
    out: list[tuple[str, Path]] = []
    for child in sorted(SKILLS_ROOT.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if name.startswith("_") or name.startswith("."):
            continue
        skill_md = child / "SKILL.md"
        skill_j2 = child / "SKILL.md.j2"
        if (skill_md.is_file() or skill_j2.is_file()) and _SKILL_NAME_RE.match(name):
            out.append((name, child))
    return out


def skill_body(name: str, skill_dir: Path, mapping: dict[str, str]) -> str:
    """Load SKILL.md, rendering .j2 templates when present."""
    j2 = skill_dir / "SKILL.md.j2"
    md = skill_dir / "SKILL.md"
    if j2.is_file():
        return _render_template(_read_text(j2), mapping)
    if md.is_file():
        return _read_text(md)
    raise FileNotFoundError(f"No SKILL.md in {skill_dir}")


def skill_install_operations(
    target: Path,
    mapping: dict[str, str],
    *,
    tools: set[str],
) -> list[tuple[str, Path, str]]:
    """Build write operations for project-level skill installs."""
    ops: list[tuple[str, Path, str]] = []
    for name, skill_dir in list_skill_dirs():
        body = skill_body(name, skill_dir, mapping)
        label = f"Skill {name}"
        if "cursor" in tools:
            ops.append(
                (
                    f"Cursor {label}",
                    target / ".cursor" / "skills" / name / "SKILL.md",
                    body,
                )
            )
        if "claude" in tools:
            ops.append(
                (
                    f"Claude {label}",
                    target / ".claude" / "skills" / name / "SKILL.md",
                    body,
                )
            )
    return ops


def global_cursor_skills_root() -> Path:
    return Path.home() / ".cursor" / "skills"


def install_global_cursor_skills(
    mapping: dict[str, str],
    *,
    dry_run: bool,
    force: bool,
    quiet: bool = False,
) -> int:
    """Install skills to ~/.cursor/skills for all-workspace availability."""
    from cli.installer import write_file

    count = 0
    for name, skill_dir in list_skill_dirs():
        path = global_cursor_skills_root() / name / "SKILL.md"
        body = skill_body(name, skill_dir, mapping)
        write_file(path, body, dry_run=dry_run, force=force, quiet=quiet)
        count += 1
    return count


def skills_index_markdown() -> str:
    """Markdown bullet list of packaged skills for docs/prompts."""
    lines = ["## Packaged Axiom skills", ""]
    for name, skill_dir in list_skill_dirs():
        md = skill_dir / "SKILL.md"
        j2 = skill_dir / "SKILL.md.j2"
        src = j2 if j2.is_file() else md
        desc = ""
        if src.is_file():
            text = _read_text(src)
            m = re.search(r"^description:\s*(.+)$", text, re.MULTILINE)
            if m:
                desc = m.group(1).strip()
        lines.append(f"- `{name}` — {desc or 'Deepiri workflow skill'}")
    lines.append("")
    return "\n".join(lines)
