#!/usr/bin/env bash
#
# Deepiri Axiom — compatibility wrapper.
# Prefer: ./install.sh
#
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
exec "$ROOT/install.sh" "$@"
