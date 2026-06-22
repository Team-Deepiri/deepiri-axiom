# Ecosystem integration guide (AXIOM)

When **ECOSYSTEM_CONTEXT** is injected (via `./setup.sh` or `setup.py install`), use it as live ground truth for this machine:

1. **Device** — GPU, WSL, container, CPU/RAM — affects local model and GPU repo recommendations (`deepiri-zepgpu`, `deepiri-gpu-utils`, Ollama).
2. **Model providers** — which API keys or local servers are available; never ask the user to paste secrets — reference env var *names* only.
3. **Local clones** — sibling `deepiri-*` / `diri-*` repos on disk; prefer these paths over guessing clone locations.
4. **Links** — inferred service relationships; use for cross-repo architecture questions.

**Refresh:** `./setup.sh`, `python3 setup.py detect --write`, or `python3 setup.py link`.

**Manifest:** `.axiom/ecosystem.json` (machine-local, gitignored).
