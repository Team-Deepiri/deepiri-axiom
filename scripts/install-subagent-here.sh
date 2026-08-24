#!/usr/bin/env bash
# Install Cursor subagent into the current directory (or TARGET=).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${TARGET:-$(pwd)}"
exec "$ROOT/install.sh" subagent --target "$TARGET" "$@"
