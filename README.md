# deepiri-axiom

Install **Deepiri **AXIOM** — the **canonical Team-Deepiri systems architect** — into your AI coding tools: **Cursor**, **Claude Code**, **GitHub Copilot**, **Gemini CLI**, and **OpenCode**. Prompts are **doc-grounded** (`docs/DOCUMENTATION_INDEX.md`, `docs/architecture/*`) and include the full **Team-Deepiri org repo map**.

- **No pip dependencies** — only Python 3.10+ stdlib.
- **Spinner** during install (disable with `--no-spinner` or in non-TTY).
- **Backups** — existing files are saved as `*.bak` before overwrite (skip with `--force`).

## CLI layout

| Path | Role |
|------|------|
| `setup.py` | Thin entry: adds repo root to `sys.path`, calls `cli.main.main()` |
| `cli/main.py` | `argparse` subcommands (`install`, `list-tools`), legacy argv normalization |
| `cli/installer.py` | Template rendering, writes, spinner, global install |
| `cli/__main__.py` | Enables `python3 -m cli` |

Same behavior as common internal CLIs: **commands** are functions (`cmd_install`, `cmd_list_tools`) bound with `set_defaults(func=...)`.

## Quick start

**One command** installs project files **and** registers the **deepiri-axiom** agent in your **user profile** so Cursor (and Gemini context) work in **any** workspace—not only `deepiri-platform`.

From the `deepiri-axiom` repo (sibling `deepiri-platform` is the default target):

```bash
python3 setup.py
# equivalent:
python3 setup.py install
python3 -m cli
python3 -m cli install
```

Explicit target:

```bash
python3 setup.py install --target /path/to/deepiri-platform
```

**Legacy:** `python3 setup.py --dry-run` is rewritten to `python3 setup.py install --dry-run` (no subcommand required).

### Subcommands

| Command | Purpose |
|---------|---------|
| `install` | Default — write templates (see flags below) |
| `list-tools` | Print PATH-based detection hints (`claude`, `gemini`, `opencode`) |

```bash
python3 setup.py list-tools
python3 -m cli list-tools
```

### `install` options

| Flag | Meaning |
|------|---------|
| `--target PATH` | Project root to install into |
| `--no-global` | **Project only** — skip `~/.cursor/agents/deepiri-axiom.md` and `~/.gemini/deepiri-axiom.md` |
| `--tools auto` | Default: cursor, claude, copilot, gemini, and opencode if `opencode` is on `PATH` |
| `--tools all` | All five tools |
| `--tools cursor,copilot` | Subset only |
| `--dry-run` | Show paths only; no writes |
| `--force` | Overwrite without `.bak` |
| `--no-spinner` | No animated progress (CI / logs) |

Auto-detect target: prefers `../deepiri-platform` next to this repo, then walks up from cwd for `deepiri-platform/` or a tree with `docs/DOCUMENTATION_INDEX.md` + `package.json`.

## What gets written

### Project (under `--target`)

| Tool | Files |
|------|--------|
| **Cursor** | `.cursor/agents/deepiri-axiom.md`, `.cursor/rules/deepiri-platform.md` |
| **Claude Code** | `CLAUDE.md` |
| **Copilot** | `.github/copilot-instructions.md` (short; review limit friendly) |
| **Gemini** | `GEMINI.md` |
| **OpenCode** | `.opencode/instructions.md`; merges `instructions` into `opencode.json` if present |

### User-level (default; omit with `--no-global`)

| Tool | Location |
|------|----------|
| **Cursor** | `~/.cursor/agents/deepiri-axiom.md` — same agent as the project; **available in every folder** after restarting Cursor if needed |
| **Gemini** | `~/.gemini/deepiri-axiom.md` — full context; if `~/.gemini/GEMINI.md` does not exist, a stub is created that points at this file |

## Contents

- `prompts/axiom-core.md` — full AXIOM master prompt (no IDE frontmatter).
- `prompts/deepiri-context.md` — Deepiri platform architecture and conventions.
- `prompts/axiom-condensed.md` — short AXIOM behavior for CLAUDE/GEMINI templates.
- `prompts/copilot-brief.md` — concise Copilot instructions.
- `templates/*.j2` — `{{PLACEHOLDER}}` templates filled by `cli/installer.py`.

Regenerate after editing prompts or templates by re-running `python3 setup.py install` (or `python3 -m cli install`).

## License

Apache License 2.0 — see [LICENSE](LICENSE). Copyright 2026 Deepiri.
