# Ecosystem auto-detection

Deepiri Axiom v2 scans your machine and sibling repos, then injects live context into every AI tool integration.

## What gets detected

| Layer | Examples |
|-------|----------|
| **Device** | OS, arch, WSL, Docker, NVIDIA GPU, Apple Silicon, CPU/RAM |
| **Model providers** | Ollama, OpenAI/Anthropic/Gemini API keys (presence only), vLLM on :8000 |
| **Apps** | Cursor, Claude Code, Gemini CLI, OpenCode, Docker, kubectl, gh |
| **Local repos** | Sibling `deepiri-*` and `diri-*` clones |
| **Links** | Inferred from local manifests (package.json, go.mod, .gitmodules, compose) — not hardcoded |

## Commands

```bash
./setup.sh                    # detect + link + install + doctor
./setup.sh --detect           # write .axiom/ecosystem.json only
python3 setup.py detect --write
python3 setup.py link
python3 setup.py status
python3 setup.py doctor
```

## Org catalog (dynamic, not hardcoded)

On scan, Axiom fetches **Team-Deepiri** public repos via `gh api` or GitHub REST (optional `GITHUB_TOKEN`), caches to `.axiom/org-catalog.json` (24h TTL), and classifies repos by name/description heuristics.

Offline or rate-limited? Uses stale cache if present.

## Local clone discovery

Not only siblings in a `Deepiri/` folder:

- Scans anchor, parents, `~/Documents/Deepiri`, `~/src`, `~/projects`, `~/code`, etc.
- Set **`DEEPIRI_CLONE_ROOTS`** (pathsep-separated) for custom clone locations
- Matches repos by **`git remote`** (`Team-Deepiri/<repo>`) even when the folder name differs

## Manifest

Machine-local JSON at `.axiom/ecosystem.json` (gitignored). Refreshed on every `./setup.sh` run.

The installer injects a markdown summary as `{{ECOSYSTEM_CONTEXT}}` in Cursor, Claude, Gemini, and OpenCode templates.
