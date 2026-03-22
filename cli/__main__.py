"""Allow: python -m cli (from deepiri-axiom repo root)."""

import sys

from cli.main import main

if __name__ == "__main__":
    raise SystemExit(main())
