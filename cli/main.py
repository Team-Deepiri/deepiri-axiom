"""CLI entry point for deepiri-axiom setup."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from cli.installer import find_default_target, run_install, tool_detection
from ecosystem.doctor import doctor_exit_code, run_doctor
from ecosystem.manifest import load_manifest, manifest_path
from ecosystem.scanner import scan_ecosystem


def _normalize_argv(argv: list[str]) -> list[str]:
    """Legacy: ``python setup.py --dry-run`` → ``python setup.py install --dry-run``."""
    if len(argv) <= 1:
        return argv + ["install"]
    known = (
        "install",
        "bootstrap",
        "list-tools",
        "subagent",
        "detect",
        "link",
        "doctor",
        "status",
    )
    if argv[1] in known:
        return argv
    return [argv[0], "install"] + argv[1:]


def cmd_install(args: argparse.Namespace) -> int:
    """Install prompts into ``--target`` and optional user-level paths."""
    if args.target is None:
        args.target = find_default_target()
    if getattr(args, "preset", "full") == "subagent":
        args.tools = "cursor"
        args.no_global = True
    args.global_install = not args.no_global
    return run_install(args)


def cmd_list_tools(_args: argparse.Namespace) -> int:
    """Print PATH-based tool detection hints."""
    d = tool_detection()
    print("Detected (optional: install uses --tools auto to skip OpenCode when missing):")
    for k, v in sorted(d.items()):
        print(f"  {k}: {v}")
    return 0


def cmd_subagent(args: argparse.Namespace) -> int:
    """Cursor subagent only: project ``.cursor/`` (+ optional user-level agent)."""
    if args.target is None:
        args.target = find_default_target()
    args.tools = "cursor"
    if getattr(args, "with_global", False):
        args.no_global = False
    else:
        args.no_global = True
    args.global_install = not args.no_global
    return run_install(args)


def cmd_detect(args: argparse.Namespace) -> int:
    """Scan device, providers, apps, and sibling repos."""
    target = (args.target or find_default_target()).resolve()
    manifest = scan_ecosystem(target, write=args.write)
    print(f"Ecosystem scan @ {target}")
    print(json.dumps(manifest.to_dict(), indent=2))
    if args.write:
        print(f"\nWrote {manifest_path(target)}")
    return 0


def cmd_link(args: argparse.Namespace) -> int:
    """Refresh ecosystem manifest and repo link graph."""
    target = (args.target or find_default_target()).resolve()
    manifest = scan_ecosystem(target, write=True)
    print(f"Linked {len(manifest.links)} relationship(s) across {len(manifest.repos)} repo(s).")
    print(f"Manifest: {manifest_path(target)}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    """Run health checks for axiom + ecosystem setup."""
    target = (args.target or find_default_target()).resolve()
    results = run_doctor(target)
    print(f"Doctor @ {target}\n")
    for r in results:
        mark = "OK" if r.ok else "FAIL"
        print(f"  [{mark}] {r.name}: {r.message}")
    return doctor_exit_code(results)


def cmd_status(args: argparse.Namespace) -> int:
    """Show current ecosystem manifest summary."""
    target = (args.target or find_default_target()).resolve()
    manifest = load_manifest(target)
    if manifest is None:
        print(f"No manifest at {manifest_path(target)} — run ./setup.sh or `setup.py detect --write`")
        return 1
    print(f"Status @ {target}")
    print(f"  generated: {manifest.generated_at}")
    print(f"  repos: {len(manifest.repos)}")
    print(f"  providers (available): {sum(1 for p in manifest.providers if p.get('available'))}")
    print(f"  links: {len(manifest.links)}")
    print(f"  recommended_tools: {', '.join(manifest.recommended_tools) or '(none)'}")
    return 0


def _add_target_argument(p: argparse.ArgumentParser) -> None:
    p.add_argument(
        "--target",
        type=Path,
        default=None,
        help="Project root (default: git root of cwd, or sibling deepiri-platform when inside axiom source)",
    )


def _add_install_arguments(p: argparse.ArgumentParser) -> None:
    _add_target_argument(p)
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
    p.add_argument(
        "--preset",
        choices=("full", "subagent"),
        default="full",
        help=(
            "subagent: same as the `subagent` subcommand (Cursor only, implies --no-global). "
            "Default full: all integrations and user-level files (unless --no-global)."
        ),
    )


def _add_install_subagent_only_arguments(p: argparse.ArgumentParser) -> None:
    _add_target_argument(p)
    p.add_argument(
        "--with-global",
        action="store_true",
        help="Also write ~/.cursor/agents/deepiri-axiom.md (no embedded repo tree; safe across workspaces).",
    )
    p.add_argument("--dry-run", action="store_true", help="Print actions without writing files")
    p.add_argument("--force", action="store_true", help="Overwrite without .bak backup")
    p.add_argument(
        "--no-spinner",
        action="store_true",
        help="Disable animated spinner (for CI or non-TTY)",
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="deepiri-axiom",
        description=(
            "Deepiri Axiom — ecosystem-aware AI architect installer for Cursor, Claude, Copilot, Gemini, OpenCode."
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

    subagent_p = subparsers.add_parser(
        "subagent",
        help="Install the Cursor subagent (and .cursor/ rules) only—fast, no Claude/Copilot/Gemini files.",
    )
    _add_install_subagent_only_arguments(subagent_p)
    subagent_p.set_defaults(func=cmd_subagent)

    list_p = subparsers.add_parser(
        "list-tools",
        help="Show which optional tools are detected on PATH.",
    )
    list_p.set_defaults(func=cmd_list_tools)

    detect_p = subparsers.add_parser(
        "detect",
        help="Scan device, model providers, apps, and sibling Deepiri repos.",
    )
    _add_target_argument(detect_p)
    detect_p.add_argument(
        "--write",
        action="store_true",
        help="Persist results to .axiom/ecosystem.json",
    )
    detect_p.set_defaults(func=cmd_detect)

    link_p = subparsers.add_parser(
        "link",
        help="Refresh .axiom/ecosystem.json and inferred repo link graph.",
    )
    _add_target_argument(link_p)
    link_p.set_defaults(func=cmd_link)

    doctor_p = subparsers.add_parser("doctor", help="Health checks for axiom + ecosystem setup.")
    _add_target_argument(doctor_p)
    doctor_p.add_argument(
        "--no-spinner",
        action="store_true",
        help="Disable animated spinner (for CI or non-TTY)",
    )
    doctor_p.set_defaults(func=cmd_doctor)

    status_p = subparsers.add_parser("status", help="Show ecosystem manifest summary.")
    _add_target_argument(status_p)
    status_p.set_defaults(func=cmd_status)

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
