#!/usr/bin/env bash
# One-shot: install the deepiri-axiom Cursor subagent into the current directory's repo.
# Usage: from the target project root, run:
#   bash /path/to/deepiri-axiom/scripts/install-subagent-here.sh
# Or with flags after -- :
#   bash .../install-subagent-here.sh -- --dry-run

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
exec python3 "$ROOT/setup.py" subagent --target "$TARGET" "$@"
