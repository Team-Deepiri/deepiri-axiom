# Deepiri Axiom

Install **Deepiri **Axiom**** — the **canonical Team-Deepiri systems architect** — into your AI coding tools: **Cursor**, **Claude Code**, **GitHub Copilot**, **Gemini CLI**, and **OpenCode**. Prompts are **doc-grounded** (`docs/DOCUMENTATION_INDEX.md`, `docs/architecture/*`) and include the full **Team-Deepiri org repo map**.

- **No pip dependencies** — only Python 3.10+ stdlib.
- **Spinner** during install (disable with `--no-spinner` or in non-TTY).
- **Backups** — existing files are saved as `*.bak` before overwrite (skip with `--force`).

## Team setup (one command for any dev)

You do **not** need to pick tools or read the rest of this doc to get started.

```bash
cd path/to/deepiri-axiom
python3 setup.py install --target /path/to/your/repo
```

That installs **every** integration (Cursor, Claude Code, Copilot, Gemini, OpenCode) into the target repo and, by default, your **user profile** (`~/.cursor/agents/deepiri-axiom.md`, `~/.gemini/deepiri-axiom.md`) so the same agents work in any folder.

Same thing, explicit name:

```bash
python3 setup.py bootstrap --target /path/to/your/repo
```

**CI / no dotfiles:** `python3 setup.py install --target . --no-global`  
**Lighter install** (skip OpenCode files unless `opencode` is on `PATH`): `--tools auto`

## CLI layout

| Path | Role |
|------|------|
| `setup.py` | Thin entry: adds repo root to `sys.path`, calls `cli.main.main()` |
| `cli/main.py` | `argparse` subcommands (`install`, `list-tools`), legacy argv normalization |
| `cli/installer.py` | Template rendering, writes, spinner, global install |
| `cli/__main__.py` | Enables `python3 -m cli` |

Same behavior as common internal CLIs: **commands** are functions (`cmd_install`, `cmd_list_tools`) bound with `set_defaults(func=...)`.

## Quick start

From the `deepiri-axiom` repo, **`deepiri-platform`** next to it is the default `--target` if that folder exists; otherwise the CLI walks up from the current directory to find a matching project root.

```bash
python3 setup.py
# equivalent:
python3 setup.py install
python3 setup.py bootstrap
python3 -m cli install
```

Explicit target (recommended in docs for clarity):

```bash
python3 setup.py install --target /path/to/deepiri-platform
```

**Legacy:** `python3 setup.py --dry-run` is rewritten to `python3 setup.py install --dry-run` (no subcommand required).

### Subcommands

| Command | Purpose |
|---------|---------|
| `install` | Write **all** tool templates (default `--tools all`) + user-level agents unless `--no-global` |
| `bootstrap` | Same as `install` — onboarding-friendly name |
| `list-tools` | Print PATH hints (`claude`, `gemini`, `opencode`); use with `--tools auto` if you want conditional OpenCode |

```bash
python3 setup.py list-tools
python3 -m cli list-tools
```

### `install` options

| Flag | Meaning |
|------|---------|
| `--target PATH` | Project root to install into |
| `--no-global` | **Project only** — skip `~/.cursor/agents/deepiri-axiom.md` and `~/.gemini/deepiri-axiom.md` |
| `--tools` | **Default: `all`** — every integration. `auto` = same but OpenCode only if `opencode` is on `PATH` |
| `--tools all` | All five tools (same as default) |
| `--tools cursor,copilot` | Subset only |
| `--dry-run` | Show paths only; no writes |
| `--force` | Overwrite without `.bak` |
| `--no-spinner` | No animated progress (CI / logs) |

Auto-detect target: prefers `../deepiri-platform` next to this repo, then walks up from cwd for `deepiri-platform/` or a tree with `docs/DOCUMENTATION_INDEX.md` + `package.json`.

## What gets written

### Project (under `--target`)

| Tool | Files |
|------|--------|
| **Cursor** | `.cursor/agents/deepiri-axiom.md`, `.cursor/rules/deepiri-axiom.mdc`; `.cursor/mcp.json` (additive merge); **`AGENTS.md`** + **`.cursorignore`** only if missing |
| **Claude Code** | `CLAUDE.md`, `CLAUDE.local.md`; `.claude/agents/`, `skills/`, `rules/`, `commands/`; `.claude/settings.json` & `settings.local.json` (Claude union-merge for `permissions.allow`) |
| **Copilot** | `.github/copilot-instructions.md`; `.github/instructions/deepiri-axiom.instructions.md` (path-scoped `applyTo` in frontmatter) |
| **Gemini** | `GEMINI.md`; `.gemini/settings.json` (additive merge); **`.geminiignore`** only if missing |
| **OpenCode** | `.opencode/instructions.md`, `agents/deepiri-axiom.md`, `commands/axiom.md`; root **`opencode.json`** (additive merge; `$schema` + `instructions` array) |

Add **`CLAUDE.local.md`** to `.gitignore` if it contains machine-only secrets. Shared instructions live in **`CLAUDE.md`**.

### Layout reference (official docs)

| Tool | Docs / layout |
|------|----------------|
| **Cursor** | [Rules](https://cursor.com/docs/context/rules), [MCP](https://cursor.com/docs/context/mcp) — `.cursor/agents`, `.cursor/rules`, `.cursor/mcp.json`, optional root `AGENTS.md`, `.cursorignore` |
| **Claude Code** | Project `.claude/` tree and `CLAUDE.md` (see Anthropic / Claude Code docs) |
| **Copilot** | [Repository custom instructions](https://docs.github.com/en/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) — `.github/copilot-instructions.md` (repo-wide), `.github/instructions/*.instructions.md` (`applyTo` globs) |
| **Gemini CLI** | [GEMINI.md](https://google-gemini.github.io/gemini-cli/docs/cli/gemini-md.html), `settings.json` — hierarchy `~/.gemini/GEMINI.md` + project `GEMINI.md`; `.gemini/settings.json`; `.geminiignore` |
| **OpenCode** | [Config](https://opencode.ai/docs/config/), [Agents](https://opencode.ai/docs/agents), [Commands](https://opencode.ai/docs/commands) — root `opencode.json`, `.opencode/agents/`, `commands/`, `instructions.md` |

Older Cursor installs may still have `.cursor/rules/deepiri-platform.md` — remove it after adopting **`deepiri-axiom.mdc`** to avoid duplicate rules.

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
- `templates/**` — `{{PLACEHOLDER}}` templates (and static snippets) filled by `cli/installer.py`.
- `templates/claude/*` — Claude Code agent, skill, rules, command, and JSON settings templates.
- `templates/cursor/*` — Cursor agent, rule (`.mdc`), `mcp.json`, `AGENTS.md`, `.cursorignore` templates.
- `templates/gemini/*` — `GEMINI.md`, `settings.json`, `geminiignore` templates.
- `templates/opencode/*` — `instructions.md`, `opencode.json`, `agents/`, `commands/` templates.
- `templates/copilot/*` — repo-wide and path-specific Copilot instruction templates.

Regenerate after editing prompts or templates by re-running `python3 setup.py install` (or `python3 -m cli install`).

## License

Apache License 2.0 — see [LICENSE](LICENSE). Copyright 2026 Deepiri.
