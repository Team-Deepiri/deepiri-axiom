# Agent instructions (deepiri-axiom)

This repository uses **deepiri-axiom** (Deepiri Genius / AXIOM). For architecture, cross-service, or doc-grounded work, use the **deepiri-axiom** custom agent (see `.cursor/agents/deepiri-axiom.md`) and project rules under `.cursor/rules/`.

- Ground platform-wide claims in **`docs/DOCUMENTATION_INDEX.md`** and **`docs/architecture/`** when those paths exist.
- Regenerate Cursor and other tool files from the **deepiri-axiom** repo: `python3 path/to/deepiri-axiom/setup.py install --target .`
