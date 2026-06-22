# Ecosystem auto-detection

Deepiri Axiom v2 scans your machine and sibling repos, then injects live context into every AI tool integration.

## What gets detected

| Layer | Examples |
|-------|----------|
| **Device** | OS, arch, WSL, Docker, NVIDIA GPU, Apple Silicon, CPU/RAM |
| **Model providers** | Ollama, OpenAI/Anthropic/Gemini API keys (presence only), vLLM on :8000 |
| **Apps** | Cursor, Claude Code, Gemini CLI, OpenCode, Docker, kubectl, gh |
| **Local repos** | Sibling `deepiri-*` and `diri-*` clones |
| **Links** | Inferred HTTP/import/grpc edges between detected repos |

## Commands

```bash
./setup.sh                    # detect + link + install + doctor
./setup.sh --detect           # write .axiom/ecosystem.json only
python3 setup.py detect --write
python3 setup.py link
python3 setup.py status
python3 setup.py doctor
```

## Manifest

Machine-local JSON at `.axiom/ecosystem.json` (gitignored). Refreshed on every `./setup.sh` run.

The installer injects a markdown summary as `{{ECOSYSTEM_CONTEXT}}` in Cursor, Claude, Gemini, and OpenCode templates.
