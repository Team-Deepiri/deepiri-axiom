---
name: deepiri-ecosystem
description: Bootstrap and read the Deepiri ecosystem manifest (.axiom/ecosystem.json).
---

# Deepiri Ecosystem

Triggers: setup, sibling repos, device/GPU, model providers, linking clones.

## Commands
```bash
./setup.sh
python3 setup.py detect --write
python3 setup.py link
python3 setup.py status
```

Prefer **detected local paths** from the manifest over guessing clone locations.
