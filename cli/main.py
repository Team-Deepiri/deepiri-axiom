"""CLI entry point for deepiri-axiom setup."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from cli.installer import find_default_target, run_install, tool_detection


def _normalize_argv(argv: list[str]) -> list[str]:
    """Legacy: ``python setup.py --dry-run`` → ``python setup.py install --dry-run``."""
    if len(argv) <= 1:
        return argv + ["install"]
    if argv[1] in ("install", "bootstrap", "list-tools"):
        return argv
    return [argv[0], "install"] + argv[1:]


def cmd_install(args: argparse.Namespace) -> int:
    """Install prompts into ``--target`` and optional user-level paths."""
    if args.target is None:
        args.target = find_default_target()
    args.global_install = not args.no_global
    return run_install(args)


def cmd_list_tools(_args: argparse.Namespace) -> int:
    """Print PATH-based tool detection hints."""
    d = tool_detection()
    print("Detected (optional: install uses --tools auto to skip OpenCode when missing):")
    for k, v in sorted(d.items()):
        print(f"  {k}: {v}")
    return 0


def _add_install_arguments(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Project directory (default: sibling deepiri-platform or auto-detect from cwd)",
    )
    p.add_argument(
        "--tools",
        default="all",
        help=(
            "Default: all — install every integration. "
            "Use auto to add OpenCode only when the opencode binary is on PATH. "
            "Or a comma list: cursor,claude,copilot,gemini,opencode"
        ),
    )
    p.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    p.add_argument("--force", action="store_true", help="Overwrite without .bak backup")
    p.add_argument(
        "--no-spinner",
        action="store_true",
        help="Disable animated spinner (for CI or non-TTY)",
    )
    p.add_argument(
        "--no-global",
        action="store_true",
        help="Skip user-level install (~/.cursor/agents, ~/.gemini). Project files only.",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deepiri-axiom",
        description=(
            "Install Deepiri Genius / AXIOM prompts for Cursor, Claude Code, Copilot, Gemini, OpenCode."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    install_p = subparsers.add_parser(
        "install",
        help="Install all tool integrations into the project (and your user profile by default).",
    )
    _add_install_arguments(install_p)
    install_p.set_defaults(func=cmd_install)

    bootstrap_p = subparsers.add_parser(
        "bootstrap",
        help="Same as install — meant for onboarding (full team setup, no thinking).",
    )
    _add_install_arguments(bootstrap_p)
    bootstrap_p.set_defaults(func=cmd_install)

    list_p = subparsers.add_parser(
        "list-tools",
        help="Show which optional tools are detected on PATH.",
    )
    list_p.set_defaults(func=cmd_list_tools)

    return parser


def main() -> int:
    """Parse argv and dispatch subcommand."""
    sys.argv = _normalize_argv(sys.argv)
    parser = _build_parser()
    args = parser.parse_args()
    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1
    return int(func(args))
