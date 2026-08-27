# Deepiri Axiom

Install **Deepiri Axiom** — the **canonical Deepiri systems architect** — into your AI tools: **Cursor**, **Claude Code**, **GitHub Copilot**, **Gemini CLI**, and **OpenCode**. Prompts are **doc-grounded** (`docs/DOCUMENTATION_INDEX.md`, `docs/architecture/*`) and carry the **full Team-Deepiri org repo map** (~50+ repos) so the installed agent can act as a **1-on-1 Deepiri expert**, with or without a local clone.

- **Ecosystem-aware** — `./install.sh` auto-detects your device, model providers, AI apps, and sibling Deepiri clones; links them into `.axiom/ecosystem.json` and injects live context into prompts.
- **No Python required for install** — pure bash (`jq` optional for JSON merge / richer manifests).
- **Backups** — existing files are saved as `*.bak` before overwrite (skip with `--force`).
- **Transparent** — the full prompt lives in [`prompts/`](prompts); there are no hidden directives.

## One command setup

```bash
git clone https://github.com/Team-Deepiri/deepiri-axiom.git
cd deepiri-axiom
./install.sh
```

`./install.sh` will:

1. Scan hardware, model providers (Ollama, API keys), and installed AI CLIs
2. Discover sibling `deepiri-*` / `diri-*` repos in your workspace
3. Write `.axiom/ecosystem.json` and inferred repo link graph
4. Install Axiom into Cursor, Claude, Copilot, Gemini, OpenCode (from detection / `--tools`)
5. Install **73 packaged skills** (gateway, Cyrex, Persola, vizult, AXIOM modes, engineering-practice skills, …) to `.cursor/skills/` and `.claude/skills/`
6. Run `doctor` health checks

Options: `--detect` (scan only), `--doctor`, `--target PATH`, `--no-global`. See `./install.sh --help`.  
(`./setup.sh` remains a thin wrapper that execs `./install.sh`.)

## 1-on-1 Deepiri expert (no target repo needed)

If you're a new contributor and haven't cloned `deepiri-control-plane` (local stack) or `deepiri-platform` (cloud portal) yet, you can still install the agent into your **user profile** and get expert Deepiri help in any folder:

```bash
git clone https://github.com/Team-Deepiri/deepiri-axiom.git
cd deepiri-axiom
./install.sh install --target . --no-global   # project only
# or, user-level included (recommended for new devs):
./install.sh install
```

The user-level install writes:

- `~/.cursor/agents/deepiri-axiom.md` — a **deepiri-axiom** agent available in every Cursor workspace.
- `~/.gemini/deepiri-axiom.md` — same context for Gemini CLI (with a stub `~/.gemini/GEMINI.md` pointer if one does not exist).

Both carry the embedded org repo map from [`prompts/deepiri-context.md`](prompts/deepiri-context.md), so you can ask questions like *"which repo owns Persola fine-tuning?"* or *"where does an external Notion webhook land?"* and get a grounded answer before you clone anything.

When you do clone a specific Deepiri repo, re-run `./install.sh install --target /path/to/that/repo` to also write **project-level** files and generate the live **target repo snapshot** alongside the org map.

## Team setup (one command for any dev)

You do **not** need to pick tools or read the rest of this doc to get started.

```bash
cd path/to/deepiri-axiom
./install.sh install --target /path/to/your/repo
```

That installs **every** integration (Cursor, Claude Code, Copilot, Gemini, OpenCode) into the target repo and, by default, your **user profile** (`~/.cursor/agents/deepiri-axiom.md`, `~/.gemini/deepiri-axiom.md`) so the same agents work in any folder.

Same thing, explicit name:

```bash
./install.sh bootstrap --target /path/to/your/repo
```

**CI / no dotfiles:** `./install.sh install --target . --no-global`  
**Lighter install** (skip OpenCode files unless `opencode` is on `PATH`): `--tools auto`

## Layout

| Path | Role |
|------|------|
| `install.sh` | **Primary entry** — detect, install, doctor, status (pure bash) |
| `setup.sh` | Compat wrapper → `install.sh` |
| `cli/` | Optional Python library (tests / advanced); not required to install |
| `cli/installer.py` | Template rendering helpers (optional; `install.sh` is the supported path) |
| `cli/skills_installer.py` | Optional Python skill installer (parity with `install.sh` skills copy) |
| `ecosystem/` | Optional scanners/doctor used by `python3 -m cli` — see `docs/ECOSYSTEM.md` |
| `skills/` | Packaged Agent Skills catalog |
| `prompts/` / `templates/` | Prompt bodies and tool templates |

## Quick start

From the `deepiri-axiom` repo, prefer sibling **`deepiri-control-plane`** (full local stack) as `--target` if present; else **`deepiri-platform`** (cloud portal); otherwise the installer walks up from the current directory to find a git root.

```bash
./install.sh
# equivalent focused installs:
./install.sh install
./install.sh bootstrap
./install.sh subagent
```

Explicit target:

```bash
./install.sh install --target /path/to/deepiri-platform
```

### Subcommands

| Command | Purpose |
|---------|---------|
| `install` | Write **all** tool templates (default `--tools all`) + user-level agents unless `--no-global` |
| `bootstrap` | Same as `install` — onboarding-friendly name |
| `subagent` | **Cursor only, fast path** — `.cursor/agents/`, `.cursor/rules/`; no Claude/Copilot/Gemini/OpenCode files. Add `--with-global` to also write `~/.cursor/agents/deepiri-axiom.md`. Same as `install --preset subagent` |
| `list-tools` | Print PATH hints (`claude`, `gemini`, `opencode`); use with `--tools auto` if you want conditional OpenCode |
| `detect` | Scan device, providers, apps, sibling repos (`--write` persists manifest) |
| `link` | Refresh `.axiom/ecosystem.json` and repo link graph |
| `doctor` | Health checks (manifest, agent install, skills pack) |
| `status` | Show ecosystem manifest summary |

### Skills library

**73 skills** in [`skills/`](skills/) install with `./install.sh` to `.cursor/skills/`, `.claude/skills/`, and `~/.cursor/skills/`. See `skills/README.md`. Regenerate catalog: `python3 scripts/generate_skills.py` (dev only).

```bash
./install.sh list-tools
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
| `--preset {full,subagent}` | `full` (default) — every integration. `subagent` — shorthand for the `subagent` subcommand (Cursor only, implies `--no-global`) |

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

- `docs/ECOSYSTEM.md` — what `./install.sh` / `detect` / `link` scan and write to `.axiom/ecosystem.json`.
- `scripts/install-subagent-here.sh` — one-shot wrapper: runs `./install.sh subagent --target <git root of cwd>` from inside any target repo.
- `scripts/generate_skills.py` — regenerates the packaged skill library in `skills/` from source (run after editing the skills catalog).
- `prompts/axiom-core.md` — full AXIOM master prompt (no IDE frontmatter).
- `prompts/deepiri-context.md` — **Deepiri Genius identity + full Team-Deepiri org repo map** (35 public repos, categorized), service boundaries, and 1-on-1 expert-mode guidance.
- `prompts/axiom-condensed.md` — short AXIOM behavior for CLAUDE/GEMINI templates (carries a one-line repo pointer).
- `prompts/copilot-brief.md` — concise Copilot instructions with a compact repo map for short-context tools.
- `prompts/axiom-branch-tools.md` — git / branch orientation policy for cross-service work.
- `templates/**` — `{{PLACEHOLDER}}` templates (and static snippets) filled by `./install.sh`.
- `templates/claude/*` — Claude Code agent, skill, rules, command, and JSON settings templates.
- `templates/cursor/*` — Cursor agent, rule (`.mdc`), `mcp.json`, `AGENTS.md`, `.cursorignore` templates.
- `templates/gemini/*` — `GEMINI.md`, `settings.json`, `geminiignore` templates.
- `templates/opencode/*` — `instructions.md`, `opencode.json`, `agents/`, `commands/` templates.
- `templates/copilot/*` — repo-wide and path-specific Copilot instruction templates.

Regenerate after editing prompts or templates by re-running `./install.sh install`.

## License

Apache License 2.0 — see [LICENSE](LICENSE). Copyright 2026 Deepiri.
