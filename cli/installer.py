"""Install templates and prompts into project and user config paths."""

from __future__ import annotations

import argparse
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
    if arg is None or arg.strip().lower() == "auto":
        tools = {"cursor", "claude", "copilot", "gemini"}
        if detect.get("opencode"):
            tools.add("opencode")
        return tools
    if arg.strip().lower() == "all":
        return {"cursor", "claude", "copilot", "gemini", "opencode"}
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


def merge_opencode_json(target: Path, dry_run: bool, force: bool, *, quiet: bool = False) -> None:
    if dry_run:
        if not quiet:
            print("  [dry-run] would merge opencode.json if present")
        return
    cfg = target / "opencode.json"
    if not cfg.is_file():
        return
    try:
        data = json.loads(cfg.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        data = {}
    if not isinstance(data, dict) or "instructions" in data:
        return
    data["instructions"] = ".opencode/instructions.md"
    backup_if_exists(cfg, force, quiet=quiet)
    cfg.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    if not quiet:
        print(f"  merged `instructions` into {cfg}")


def run_global_install(
    args: argparse.Namespace,
    mapping: dict[str, str],
    tools: set[str],
    use_spinner: bool,
) -> None:
    """Register configs under ``~/.cursor`` and ``~/.gemini`` when not ``--no-global``."""
    global_ops: list[tuple[str, Path, str]] = []

    if "cursor" in tools:
        body = render_template(read_text(TEMPLATES / "cursor-agent.md.j2"), mapping)
        global_ops.append(("User Cursor agent (all workspaces)", global_cursor_agent_path(), body))

    if "gemini" in tools:
        body = render_template(read_text(TEMPLATES / "gemini.md.j2"), mapping)
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
                render_template(read_text(TEMPLATES / "cursor-agent.md.j2"), mapping),
            )
        )
        operations.append(
            (
                "Cursor rules",
                target / ".cursor" / "rules" / "deepiri-platform.md",
                render_template(read_text(TEMPLATES / "cursor-rule.md.j2"), mapping),
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

    if "copilot" in tools:
        operations.append(
            (
                "Copilot instructions",
                target / ".github" / "copilot-instructions.md",
                render_template(read_text(TEMPLATES / "copilot-instructions.md.j2"), mapping),
            )
        )

    if "gemini" in tools:
        operations.append(
            (
                "GEMINI.md",
                target / "GEMINI.md",
                render_template(read_text(TEMPLATES / "gemini.md.j2"), mapping),
            )
        )

    if "opencode" in tools:
        operations.append(
            (
                "OpenCode instructions",
                target / ".opencode" / "instructions.md",
                render_template(read_text(TEMPLATES / "opencode-instructions.md.j2"), mapping),
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

    if "opencode" in tools:
        if use_spinner:
            with Spinner("OpenCode opencode.json…", enabled=True):
                merge_opencode_json(target, args.dry_run, args.force, quiet=True)
            if not args.dry_run and (target / "opencode.json").is_file():
                cfg = target / "opencode.json"
                try:
                    data = json.loads(cfg.read_text(encoding="utf-8"))
                except json.JSONDecodeError:
                    data = {}
                if isinstance(data, dict) and data.get("instructions") == ".opencode/instructions.md":
                    print(f"  merged `instructions` into {cfg}")
        else:
            merge_opencode_json(target, args.dry_run, args.force, quiet=False)

    if getattr(args, "global_install", True):
        run_global_install(args, mapping, tools, use_spinner)

    print("Done.")
    return 0
