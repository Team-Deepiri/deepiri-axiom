# Deepiri Axiom skills library

**46 packaged skills** installed by `./setup.sh` into:

| Target | Path |
|--------|------|
| Cursor (project) | `.cursor/skills/<name>/SKILL.md` |
| Claude Code (project) | `.claude/skills/<name>/SKILL.md` |
| Cursor (global) | `~/.cursor/skills/<name>/SKILL.md` |

Regenerate static skills after editing the catalog:

```bash
python3 scripts/generate_skills.py
```

`deepiri-axiom` uses `SKILL.md.j2` for full prompt injection at install time.

## Categories

- **Platform** — gateway, auth, core-api, external-bridge, web-frontend, language-intelligence
- **AI runtime** — cyrex, persola, helox, modelkit, prismpipe, synapse, training, guardrails, toolbox
- **Infrastructure** — vizult, cascade, conduit, wooven, memorymesh, ollama, gpu/zepgpu
- **AXIOM modes** — scan, architect, debug, refactor, review
- **DX** — ecosystem, doc-grounding, service-boundaries, compose, skaffold, cross-repo
- **Products** — aarflingo, polylogue, sorge, boardman, huddle, tombstone, emotion, renderflow, egottol
