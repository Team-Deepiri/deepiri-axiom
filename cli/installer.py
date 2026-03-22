"""Install templates and prompts into project and user config paths."""

from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import sys
import threading
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROMPTS = REPO_ROOT / "prompts"
TEMPLATES = REPO_ROOT / "templates"


class Spinner:
    """Terminal spinner (threading). Disabled with ``quiet`` or non-TTY."""

    FRAMES = ("|", "/", "-", "\\")

    def __init__(self, message: str = "", *, enabled: bool = True, interval: float = 0.09) -> None:
        self.message = message
        self.enabled = enabled and sys.stdout.isatty()
        self.interval = interval
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None
        self._lock = threading.Lock()

    def _run(self) -> None:
        i = 0
        while not self._stop.wait(self.interval):
            with self._lock:
                msg = self.message
            frame = self.FRAMES[i % len(self.FRAMES)]
            sys.stdout.write(f"\r{frame} {msg}" + " " * max(0, 8))
            sys.stdout.flush()
            i += 1

    def __enter__(self) -> Spinner:
        if self.enabled:
            self._stop.clear()
            self._thread = threading.Thread(target=self._run, daemon=True)
            self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        if not self.enabled:
            return
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=3.0)
        sys.stdout.write("\r" + " " * (len(self.message) + 8) + "\r")
        sys.stdout.flush()

    def update(self, message: str) -> None:
        with self._lock:
            self.message = message


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_template(template_body: str, mapping: dict[str, str]) -> str:
    out = template_body
    for key, val in mapping.items():
        out = out.replace("{{" + key + "}}", val)
    missing = re.findall(r"\{\{([A-Z0-9_]+)\}\}", out)
    if missing:
        raise ValueError(f"Unresolved template placeholders: {sorted(set(missing))}")
    return out


def find_default_target() -> Path:
    """Prefer sibling ``deepiri-platform`` when running from the deepiri-axiom repo."""
    sibling = REPO_ROOT.parent / "deepiri-platform"
    if sibling.is_dir():
        return sibling
    cwd = Path.cwd()
    for base in [cwd, *cwd.parents]:
        candidate = base / "deepiri-platform"
        if candidate.is_dir():
            return candidate
        if (base / "docs" / "DOCUMENTATION_INDEX.md").is_file() and (base / "package.json").is_file():
            return base
    return cwd


def tool_detection() -> dict[str, bool]:
    return {
        "cursor": True,
        "claude": shutil.which("claude") is not None,
        "copilot": True,
        "gemini": shutil.which("gemini") is not None,
        "opencode": shutil.which("opencode") is not None,
    }


def parse_tools_arg(arg: str | None, detect: dict[str, bool]) -> set[str]:
    if arg is None or not str(arg).strip():
        return {"cursor", "claude", "copilot", "gemini", "opencode"}
    a = arg.strip().lower()
    if a == "all":
        return {"cursor", "claude", "copilot", "gemini", "opencode"}
    if a == "auto":
        tools = {"cursor", "claude", "copilot", "gemini"}
        if detect.get("opencode"):
            tools.add("opencode")
        return tools
    out: set[str] = set()
    for part in arg.split(","):
        p = part.strip().lower()
        if not p:
            continue
        if p not in ("cursor", "claude", "copilot", "gemini", "opencode"):
            raise SystemExit(
                f"Unknown tool: {p!r}. Use: cursor, claude, copilot, gemini, opencode, all, auto."
            )
        out.add(p)
    return out


def backup_if_exists(path: Path, force: bool, *, quiet: bool = False) -> None:
    if not path.is_file():
        return
    if force:
        return
    bak = path.with_suffix(path.suffix + ".bak")
    n = 1
    while bak.exists():
        bak = path.with_suffix(f"{path.suffix}.bak.{n}")
        n += 1
    shutil.copy2(path, bak)
    if not quiet:
        print(f"  (backup: {bak})")


def write_file(
    path: Path,
    content: str,
    *,
    dry_run: bool,
    force: bool,
    quiet: bool = False,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        if not quiet:
            print(f"  [dry-run] would write {path} ({len(content)} bytes)")
        return
    if path.exists():
        backup_if_exists(path, force, quiet=quiet)
    path.write_text(content, encoding="utf-8")
    if not quiet:
        print(f"  wrote {path}")


def global_cursor_agent_path() -> Path:
    return Path.home() / ".cursor" / "agents" / "deepiri-axiom.md"


def global_gemini_context_path() -> Path:
    return Path.home() / ".gemini" / "deepiri-axiom.md"


def merge_claude_settings(existing: dict, default: dict) -> dict:
    """Deep-merge Claude Code JSON: union ``permissions.allow``; fill missing keys from ``default``."""
    out = copy.deepcopy(existing) if isinstance(existing, dict) else {}
    if not isinstance(default, dict):
        return out
    for k, v in default.items():
        if k == "permissions" and isinstance(v, dict):
            out.setdefault("permissions", {})
            if not isinstance(out["permissions"], dict):
                out["permissions"] = {}
            op = out["permissions"]
            if "allow" in v and isinstance(v.get("allow"), list):
                cur = op.get("allow", [])
                if not isinstance(cur, list):
                    cur = []
                merged_allow = sorted(set(cur) | set(v["allow"]))
                op["allow"] = merged_allow
            for pk, pv in v.items():
                if pk != "allow" and pk not in op:
                    op[pk] = copy.deepcopy(pv)
        elif k not in out:
            out[k] = copy.deepcopy(v)
    return out


def merge_json_fill_missing(existing: dict, default: dict) -> dict:
    """Recursively merge dicts: only add keys missing in ``existing`` (additive project JSON)."""
    out = copy.deepcopy(existing) if isinstance(existing, dict) else {}
    if not isinstance(default, dict):
        return out
    for k, v in default.items():
        if k not in out:
            out[k] = copy.deepcopy(v)
        elif isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = merge_json_fill_missing(out[k], v)
    return out


def write_json_merge_fill_missing(
    path: Path,
    template_rel: str,
    *,
    dry_run: bool,
    force: bool,
    quiet: bool = False,
) -> None:
    """Write or merge JSON from ``templates/<template_rel>``; additive merge unless ``--force``."""
    default = json.loads(read_text(TEMPLATES / template_rel))
    if dry_run:
        if not quiet:
            print(f"  [dry-run] would write/merge {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
        if not isinstance(existing, dict):
            existing = {}
        merged = merge_json_fill_missing(existing, default)
        backup_if_exists(path, force=False, quiet=quiet)
        path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
        if not quiet:
            print(f"  merged {path}")
    else:
        if path.exists():
            backup_if_exists(path, force, quiet=quiet)
        path.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        if not quiet:
            print(f"  wrote {path}")


def merge_cursor_mcp_json(existing: dict, default: dict) -> dict:
    """Merge project ``.cursor/mcp.json``: add missing ``mcpServers`` entries only; keep existing servers."""
    out = copy.deepcopy(existing) if isinstance(existing, dict) else {}
    if not isinstance(default, dict):
        return out
    for k, v in default.items():
        if k == "mcpServers" and isinstance(v, dict):
            out.setdefault("mcpServers", {})
            if not isinstance(out["mcpServers"], dict):
                out["mcpServers"] = {}
            for name, srv in v.items():
                if name not in out["mcpServers"]:
                    out["mcpServers"][name] = copy.deepcopy(srv)
        elif k not in out:
            out[k] = copy.deepcopy(v)
    return out


def write_cursor_mcp_json(
    path: Path,
    template_filename: str,
    *,
    dry_run: bool,
    force: bool,
    quiet: bool = False,
) -> None:
    """Write or merge ``.cursor/mcp.json`` from packaged template (additive ``mcpServers``)."""
    default = json.loads(read_text(TEMPLATES / "cursor" / template_filename))
    if dry_run:
        if not quiet:
            print(f"  [dry-run] would write/merge {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
        if not isinstance(existing, dict):
            existing = {}
        merged = merge_cursor_mcp_json(existing, default)
        backup_if_exists(path, force=False, quiet=quiet)
        path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
        if not quiet:
            print(f"  merged {path}")
    else:
        if path.exists():
            backup_if_exists(path, force, quiet=quiet)
        path.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        if not quiet:
            print(f"  wrote {path}")


def write_file_if_absent(
    path: Path,
    content: str,
    *,
    dry_run: bool,
    quiet: bool = False,
) -> None:
    """Write ``path`` only if it does not exist (for ``AGENTS.md``, ``.cursorignore`` stubs)."""
    if path.exists():
        return
    if dry_run:
        if not quiet:
            print(f"  [dry-run] would write {path} (only if missing)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if not quiet:
        print(f"  wrote {path} (new)")


def write_claude_json(
    path: Path,
    template_filename: str,
    *,
    dry_run: bool,
    force: bool,
    quiet: bool = False,
) -> None:
    """Write or merge ``.claude/settings*.json`` from packaged templates."""
    default = json.loads(read_text(TEMPLATES / "claude" / template_filename))
    if dry_run:
        if not quiet:
            print(f"  [dry-run] would write/merge {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = {}
        if not isinstance(existing, dict):
            existing = {}
        merged = merge_claude_settings(existing, default)
        backup_if_exists(path, force=False, quiet=quiet)
        path.write_text(json.dumps(merged, indent=2) + "\n", encoding="utf-8")
        if not quiet:
            print(f"  merged {path}")
    else:
        if path.exists():
            backup_if_exists(path, force, quiet=quiet)
        path.write_text(json.dumps(default, indent=2) + "\n", encoding="utf-8")
        if not quiet:
            print(f"  wrote {path}")


def run_global_install(
    args: argparse.Namespace,
    mapping: dict[str, str],
    tools: set[str],
    use_spinner: bool,
) -> None:
    """Register configs under ``~/.cursor`` and ``~/.gemini`` when not ``--no-global``."""
    global_ops: list[tuple[str, Path, str]] = []

    if "cursor" in tools:
        body = render_template(read_text(TEMPLATES / "cursor" / "agent.md.j2"), mapping)
        global_ops.append(("User Cursor agent (all workspaces)", global_cursor_agent_path(), body))

    if "gemini" in tools:
        body = render_template(read_text(TEMPLATES / "gemini" / "GEMINI.md.j2"), mapping)
        global_ops.append(("User Gemini context", global_gemini_context_path(), body))

    if not global_ops:
        return

    print()
    print("User-level (available in any project / workspace):")

    if use_spinner:
        with Spinner("Registering user-level tools…", enabled=True) as sp:
            for label, path, body in global_ops:
                sp.update(f"{label}…")
                write_file(path, body, dry_run=args.dry_run, force=args.force, quiet=True)
        for _label, path, body in global_ops:
            if args.dry_run:
                print(f"  [dry-run] would write {path} ({len(body)} bytes)")
            else:
                print(f"  wrote {path}")
    else:
        for _label, path, body in global_ops:
            write_file(path, body, dry_run=args.dry_run, force=args.force, quiet=False)

    if not args.dry_run and "gemini" in tools:
        gem = Path.home() / ".gemini" / "GEMINI.md"
        marker = "deepiri-axiom-context"
        if not gem.is_file():
            gem.parent.mkdir(parents=True, exist_ok=True)
            stub = (
                "# Global Gemini context (deepiri-axiom)\n\n"
                f"<!-- {marker} -->\n"
                "Full Deepiri AXIOM instructions are in:\n"
                f"  {global_gemini_context_path()}\n\n"
                "If your Gemini CLI supports `@file` or includes, reference that path; "
                "otherwise merge the sections you need into this file.\n"
            )
            gem.write_text(stub, encoding="utf-8")
            print(f"  created {gem} (stub pointing at deepiri-axiom context)")
        else:
            print(
                f"  Gemini: optional — merge or @-include {global_gemini_context_path()} into {gem}"
            )

    if "cursor" in tools and not args.dry_run:
        print()
        print(
            "Cursor: open any folder — Agent list should include **deepiri-axiom** "
            f"({global_cursor_agent_path()}). Restart Cursor if it does not appear."
        )


def run_install(args: argparse.Namespace) -> int:
    """Write project and optional user-level template outputs."""
    target: Path = args.target.resolve()
    detect = tool_detection()
    tools = parse_tools_arg(args.tools, detect)

    axiom_core = read_text(PROMPTS / "axiom-core.md")
    deepiri_ctx = read_text(PROMPTS / "deepiri-context.md")
    axiom_condensed = read_text(PROMPTS / "axiom-condensed.md")
    copilot_brief = read_text(PROMPTS / "copilot-brief.md")

    mapping = {
        "DEEPIRI_CONTEXT": deepiri_ctx,
        "AXIOM_CORE": axiom_core,
        "AXIOM_CONDENSED": axiom_condensed,
        "COPILOT_BRIEF": copilot_brief,
    }

    use_spinner = not args.no_spinner

    operations: list[tuple[str, Path, str]] = []

    if "cursor" in tools:
        operations.append(
            (
                "Cursor agent",
                target / ".cursor" / "agents" / "deepiri-axiom.md",
                render_template(read_text(TEMPLATES / "cursor" / "agent.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Cursor rule (.mdc)",
                target / ".cursor" / "rules" / "deepiri-axiom.mdc",
                render_template(read_text(TEMPLATES / "cursor" / "rules-deepiri-axiom.md.j2"), mapping),
            )
        )

    if "claude" in tools:
        operations.append(
            (
                "CLAUDE.md",
                target / "CLAUDE.md",
                render_template(read_text(TEMPLATES / "claude.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "CLAUDE.local.md",
                target / "CLAUDE.local.md",
                render_template(read_text(TEMPLATES / "claude" / "CLAUDE.local.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Claude Code agent",
                target / ".claude" / "agents" / "deepiri-axiom.md",
                render_template(read_text(TEMPLATES / "claude" / "agent.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Claude Code skill",
                target / ".claude" / "skills" / "deepiri-axiom" / "SKILL.md",
                render_template(read_text(TEMPLATES / "claude" / "skills-SKILL.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Claude Code rules",
                target / ".claude" / "rules" / "deepiri-axiom.md",
                render_template(read_text(TEMPLATES / "claude" / "rules.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Claude Code command (axiom)",
                target / ".claude" / "commands" / "axiom.md",
                read_text(TEMPLATES / "claude" / "command-axiom.md"),
            )
        )

    if "copilot" in tools:
        operations.append(
            (
                "Copilot instructions (repo-wide)",
                target / ".github" / "copilot-instructions.md",
                render_template(read_text(TEMPLATES / "copilot" / "copilot-instructions.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Copilot path-specific instructions",
                target / ".github" / "instructions" / "deepiri-axiom.instructions.md",
                render_template(
                    read_text(TEMPLATES / "copilot" / "instructions-deepiri-axiom.instructions.md.j2"),
                    mapping,
                ),
            )
        )

    if "gemini" in tools:
        operations.append(
            (
                "GEMINI.md",
                target / "GEMINI.md",
                render_template(read_text(TEMPLATES / "gemini" / "GEMINI.md.j2"), mapping),
            )
        )

    if "opencode" in tools:
        operations.append(
            (
                "OpenCode instructions",
                target / ".opencode" / "instructions.md",
                render_template(read_text(TEMPLATES / "opencode" / "instructions.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "OpenCode agent",
                target / ".opencode" / "agents" / "deepiri-axiom.md",
                render_template(read_text(TEMPLATES / "opencode" / "agents" / "deepiri-axiom.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "OpenCode command (axiom)",
                target / ".opencode" / "commands" / "axiom.md",
                read_text(TEMPLATES / "opencode" / "commands" / "axiom.md"),
            )
        )

    print(f"Target: {target}")
    print(f"Tools: {', '.join(sorted(tools))}")
    print()

    if use_spinner:
        with Spinner("deepiri-axiom…", enabled=True) as sp:
            for label, path, body in operations:
                sp.update(f"{label}…")
                write_file(path, body, dry_run=args.dry_run, force=args.force, quiet=True)
        for _label, path, body in operations:
            if args.dry_run:
                print(f"  [dry-run] would write {path} ({len(body)} bytes)")
            else:
                print(f"  wrote {path}")
    else:
        for _label, path, body in operations:
            write_file(path, body, dry_run=args.dry_run, force=args.force, quiet=False)

    if "cursor" in tools:
        mcp_path = target / ".cursor" / "mcp.json"
        ci_path = target / ".cursorignore"
        agents_path = target / "AGENTS.md"
        ci_body = read_text(TEMPLATES / "cursor" / "cursorignore")
        agents_body = read_text(TEMPLATES / "cursor" / "AGENTS.md")
        ci_missing = not ci_path.exists()
        agents_missing = not agents_path.exists()
        if use_spinner:
            with Spinner("Cursor project config…", enabled=True):
                write_cursor_mcp_json(
                    mcp_path,
                    "mcp.json",
                    dry_run=args.dry_run,
                    force=args.force,
                    quiet=True,
                )
                write_file_if_absent(ci_path, ci_body, dry_run=args.dry_run, quiet=True)
                write_file_if_absent(agents_path, agents_body, dry_run=args.dry_run, quiet=True)
            if args.dry_run:
                print(f"  [dry-run] would write/merge {mcp_path}")
                if ci_missing:
                    print(f"  [dry-run] would write {ci_path} (only if missing)")
                if agents_missing:
                    print(f"  [dry-run] would write {agents_path} (only if missing)")
            else:
                print(f"  wrote/merged {mcp_path}")
                if ci_missing:
                    print(f"  wrote {ci_path} (new)")
                if agents_missing:
                    print(f"  wrote {agents_path} (new)")
        else:
            write_cursor_mcp_json(
                mcp_path,
                "mcp.json",
                dry_run=args.dry_run,
                force=args.force,
                quiet=False,
            )
            write_file_if_absent(ci_path, ci_body, dry_run=args.dry_run, quiet=False)
            write_file_if_absent(agents_path, agents_body, dry_run=args.dry_run, quiet=False)

    if "claude" in tools:
        s_json = target / ".claude" / "settings.json"
        s_local = target / ".claude" / "settings.local.json"
        if use_spinner:
            with Spinner("Claude Code settings…", enabled=True):
                write_claude_json(
                    s_json,
                    "settings.json",
                    dry_run=args.dry_run,
                    force=args.force,
                    quiet=True,
                )
                write_claude_json(
                    s_local,
                    "settings.local.json",
                    dry_run=args.dry_run,
                    force=args.force,
                    quiet=True,
                )
            if args.dry_run:
                print(f"  [dry-run] would write/merge {s_json}")
                print(f"  [dry-run] would write/merge {s_local}")
            else:
                print(f"  wrote/merged {s_json}")
                print(f"  wrote/merged {s_local}")
        else:
            write_claude_json(
                s_json,
                "settings.json",
                dry_run=args.dry_run,
                force=args.force,
                quiet=False,
            )
            write_claude_json(
                s_local,
                "settings.local.json",
                dry_run=args.dry_run,
                force=args.force,
                quiet=False,
            )

    if "gemini" in tools:
        gset = target / ".gemini" / "settings.json"
        gignore = target / ".geminiignore"
        gignore_body = read_text(TEMPLATES / "gemini" / "geminiignore")
        gignore_missing = not gignore.exists()
        if use_spinner:
            with Spinner("Gemini project config…", enabled=True):
                write_json_merge_fill_missing(
                    gset,
                    "gemini/settings.json",
                    dry_run=args.dry_run,
                    force=args.force,
                    quiet=True,
                )
                write_file_if_absent(gignore, gignore_body, dry_run=args.dry_run, quiet=True)
            if args.dry_run:
                print(f"  [dry-run] would write/merge {gset}")
                if gignore_missing:
                    print(f"  [dry-run] would write {gignore} (only if missing)")
            else:
                print(f"  wrote/merged {gset}")
                if gignore_missing:
                    print(f"  wrote {gignore} (new)")
        else:
            write_json_merge_fill_missing(
                gset,
                "gemini/settings.json",
                dry_run=args.dry_run,
                force=args.force,
                quiet=False,
            )
            write_file_if_absent(gignore, gignore_body, dry_run=args.dry_run, quiet=False)

    if "opencode" in tools:
        oc_path = target / "opencode.json"
        if use_spinner:
            with Spinner("OpenCode opencode.json…", enabled=True):
                write_json_merge_fill_missing(
                    oc_path,
                    "opencode/opencode.json",
                    dry_run=args.dry_run,
                    force=args.force,
                    quiet=True,
                )
            if args.dry_run:
                print(f"  [dry-run] would write/merge {oc_path}")
            else:
                print(f"  wrote/merged {oc_path}")
        else:
            write_json_merge_fill_missing(
                oc_path,
                "opencode/opencode.json",
                dry_run=args.dry_run,
                force=args.force,
                quiet=False,
            )

    if getattr(args, "global_install", True):
        run_global_install(args, mapping, tools, use_spinner)

    print("Done.")
    return 0
