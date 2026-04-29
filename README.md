# Deepiri Axiom

Install **Deepiri Axiom** — the **canonical Team-Deepiri systems architect** — into your AI coding tools: **Cursor**, **Claude Code**, **GitHub Copilot**, **Gemini CLI**, and **OpenCode**. Prompts are **doc-grounded** (`docs/DOCUMENTATION_INDEX.md`, `docs/architecture/*` where they exist) and include the **Team-Deepiri org map** in `deepiri-context.md`.

- **No pip dependencies** — only Python 3.10+ stdlib.
- **Spinner** during install (disable with `--no-spinner` or in non-TTY).
- **Backups** — existing files are saved as `*.bak` before overwrite (skip with `--force`).

## Cursor subagent (fastest path)

**Goal:** get **`.cursor/agents/deepiri-axiom.md`** (and project rules) so you can pick **deepiri-axiom** in Cursor’s custom subagent list—no other tools, no `~/.cursor` copy unless you ask.

```bash
cd /path/to/your/repo
python3 /path/to/deepiri-axiom/setup.py subagent
```

- **From any subfolder of the repo** (with git), use: `bash /path/to/deepiri-axiom/scripts/install-subagent-here.sh` — it resolves the git root and runs `subagent` for you.
- **Optional user-level** agent (same prompt, but **no** embedded repo tree in that file): `python3 .../setup.py subagent --with-global`
- **Same as:** `python3 .../setup.py install --preset subagent`

Then in **Cursor:** open the subagent / custom agent picker and choose **deepiri-axiom**; restart Cursor if it does not appear.

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
| `cli/main.py` | `argparse` subcommands (`install`, `bootstrap`, `subagent`, `list-tools`), legacy argv normalization |
| `scripts/install-subagent-here.sh` | Resolves git root and runs `subagent` (convenience) |
| `cli/installer.py` | Template rendering, writes, spinner, global install |
| `cli/__main__.py` | Enables `python3 -m cli` |

Same behavior as common internal CLIs: **commands** are functions (`cmd_install`, `cmd_list_tools`) bound with `set_defaults(func=...)`.

## Quick start

**Default `--target`:** the **git root of your current working directory** (or `cwd` if not in a git repo). The only exception is when you run the CLI **from inside the `deepiri-axiom` source tree**—then the default is a sibling `../deepiri-platform` if that directory exists (dogfooding the installer).

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
| `subagent` | **Cursor only** (project `.cursor/`), implies `--no-global` unless you pass `--with-global` |
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
| `--preset subagent` | Same as the `subagent` subcommand (Cursor only, project-only) |

Auto-detect `--target`: **git root of `cwd`**, except when the shell is under the `deepiri-axiom` checkout (then default is `../deepiri-platform` if present).

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
| **Cursor** | `~/.cursor/agents/deepiri-axiom.md` — same instructions as the project agent, but **without** a frozen repo tree (so it is not wrong when you open other folders) |
| **Gemini** | `~/.gemini/deepiri-axiom.md` — same idea; if `~/.gemini/GEMINI.md` does not exist, a stub is created that points at this file |

## Contents

- `prompts/axiom-core.md` — full AXIOM master prompt (no IDE frontmatter).
- `prompts/deepiri-context.md` — Deepiri org layout: platform + major product areas + a **Team-Deepiri** repo table (regenerate: `gh api orgs/Team-Deepiri/repos --paginate`). Always doc-grounded per target repo.
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
