#!/usr/bin/env bash
#
# Deepiri Axiom — one-shot ecosystem bootstrap.
#
#   ./setup.sh              Detect device/providers/repos, link ecosystem, install agents.
#   ./setup.sh --detect     Scan only (writes .axiom/ecosystem.json).
#   ./setup.sh --doctor     Health checks.
#   ./setup.sh --target DIR Install into another repo (default: auto).
#   ./setup.sh --no-global  Project-only install (skip ~/.cursor, ~/.gemini).
#   ./setup.sh --help       Show this help.
#
set -euo pipefail

if [ -t 1 ]; then
  BOLD="$(printf '\033[1m')"; GREEN="$(printf '\033[32m')"
  YELLOW="$(printf '\033[33m')"; RED="$(printf '\033[31m')"; RESET="$(printf '\033[0m')"
else
  BOLD=""; GREEN=""; YELLOW=""; RED=""; RESET=""
fi
info()  { printf '%s\n' "${GREEN}==>${RESET} ${BOLD}$*${RESET}"; }
warn()  { printf '%s\n' "${YELLOW}warning:${RESET} $*"; }
die()   { printf '%s\n' "${RED}error:${RESET} $*" >&2; exit 1; }

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

DETECT_ONLY=0
DOCTOR=0
NO_GLOBAL=0
TARGET=""

while [ $# -gt 0 ]; do
  case "$1" in
    --detect) DETECT_ONLY=1; shift ;;
    --doctor) DOCTOR=1; shift ;;
    --no-global) NO_GLOBAL=1; shift ;;
    --target)
      shift
      TARGET="${1:-}"
      [ -n "$TARGET" ] || die "--target requires a path"
      shift
      ;;
    --help|-h)
      sed -n '2,11p' "$0" | sed 's/^# \{0,1\}//'
      exit 0
      ;;
    *) die "unknown option: $1 (try --help)" ;;
  esac
done

ensure_python() {
  command -v python3 >/dev/null 2>&1 || die "python3 is required (3.10+)."
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
    || die "Python 3.10+ required."
  info "Python $(python3 --version | cut -d' ' -f2)"
}

run_detect() {
  local detect_args=(detect --write --no-spinner)
  [ -n "$TARGET" ] && detect_args+=(--target "$TARGET")
  python3 setup.py "${detect_args[@]}"
}

run_install() {
  local install_args=(install --no-spinner)
  [ -n "$TARGET" ] && install_args+=(--target "$TARGET")
  [ "$NO_GLOBAL" -eq 1 ] && install_args+=(--no-global)

  local tools=""
  if [ -f "$REPO_ROOT/.axiom/ecosystem.json" ]; then
    tools="$(python3 -c "
import json
from pathlib import Path
p = Path('$REPO_ROOT/.axiom/ecosystem.json')
d = json.loads(p.read_text())
t = d.get('recommended_tools') or []
print(','.join(t) if t else '')
" 2>/dev/null || true)"
  fi
  if [ -n "$tools" ]; then
    info "Auto-selected tools: $tools"
    install_args+=(--tools "$tools")
  else
    install_args+=(--tools auto)
  fi
  python3 setup.py "${install_args[@]}"
}

run_doctor() {
  local doc_args=(doctor --no-spinner)
  [ -n "$TARGET" ] && doc_args+=(--target "$TARGET")
  python3 setup.py "${doc_args[@]}"
}

ensure_python

if [ "$DOCTOR" -eq 1 ]; then
  run_doctor
  exit $?
fi

info "Scanning Deepiri ecosystem (device, providers, apps, sibling repos)..."
run_detect

if [ "$DETECT_ONLY" -eq 1 ]; then
  info "Detect-only complete. Manifest: .axiom/ecosystem.json"
  exit 0
fi

info "Installing Deepiri Axiom into AI tools..."
run_install

info "Running doctor..."
run_doctor || warn "Some checks failed — see messages above."

info "Done."
info "Re-run anytime: ${BOLD}./setup.sh${RESET}"
info "Status: ${BOLD}python3 setup.py status${RESET}"
