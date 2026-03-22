#!/usr/bin/env python3
"""
deepiri-axiom — setup CLI entry point.

Delegates to :mod:`cli.main`. Run from repo root::

    python3 setup.py              # full install (all tools), default target
    python3 setup.py install
    python3 setup.py bootstrap    # same as install
    python3 setup.py list-tools
    python3 -m cli
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is importable when executed as a script.
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from cli.main import main

if __name__ == "__main__":
    raise SystemExit(main())
