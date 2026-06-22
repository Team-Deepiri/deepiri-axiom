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
  YELLOW="$(printf '\033[33m')"; RED="$(printf '\033[31m')"
  CYAN="$(printf '\033[36m')"; DIM="$(printf '\033[2m')"; RESET="$(printf '\033[0m')"
else
  BOLD=""; GREEN=""; YELLOW=""; RED=""; CYAN=""; DIM=""; RESET=""
fi

info()  { printf '%s\n' "${GREEN}==>${RESET} ${BOLD}$*${RESET}"; }
warn()  { printf '%s\n' "${YELLOW}warning:${RESET} $*"; }
die()   { printf '%s\n' "${RED}error:${RESET} $*" >&2; exit 1; }

# First-person Axiom voice — the subagent talking to you.
axiom_say() {
  local line
  while IFS= read -r line || [ -n "$line" ]; do
    [ -z "$line" ] && printf '\n' && continue
    printf '%s\n' "${CYAN}AXIOM${RESET} ${DIM}|${RESET} $line"
  done <<< "$1"
}

axiom_pause() {
  [ -t 1 ] || return 0
  sleep 0.4
}

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

manifest_summary() {
  local manifest_path="$1"
  [ -f "$manifest_path" ] || return 0
  python3 -c "
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
d = json.loads(p.read_text())
dev = d.get('device') or {}
repos = [r.get('name','') for r in d.get('repos') or [] if r.get('name')]
providers = [p.get('name','') for p in d.get('providers') or [] if p.get('available')]
tools = d.get('recommended_tools') or []
gpu = 'yes' if dev.get('has_nvidia_gpu') else 'no'
print(f'GPU:{gpu}')
print(f'ARCH:{dev.get(\"arch\",\"?\")}')
print(f'WSL:{dev.get(\"is_wsl\", False)}')
print(f'REPOS:{len(repos)}')
if repos:
    print('REPO_NAMES:' + ','.join(repos[:8]))
    if len(repos) > 8:
        print(f'REPO_MORE:{len(repos) - 8}')
print(f'PROVIDERS:{len(providers)}')
if providers:
    print('PROVIDER_NAMES:' + ','.join(providers[:6]))
print('TOOLS:' + ','.join(tools))
" "$manifest_path" 2>/dev/null || true
}

axiom_intro_full() {
  axiom_say "Hi — I'm ${BOLD}Deepiri Axiom${RESET}. I'm your systems-architect subagent for the whole Team-Deepiri ecosystem."
  axiom_pause
  axiom_say "I'm not a generic chatbot. I know which repo owns what — gateway vs Cyrex vs Persola, service boundaries, ports, the org map. When you ask me architecture questions, I ground on docs and live code, not vibes."
  axiom_pause
  axiom_say "You ran ./setup.sh, so I'm going to wire myself into your machine: scan your hardware, see which model providers you actually have, find sibling deepiri-* clones nearby, and install me into whatever AI tools you're already using."
  axiom_pause
  if [ -n "$TARGET" ]; then
    axiom_say "You pointed me at ${BOLD}${TARGET}${RESET}. I'll treat that as home base for this install."
  else
    axiom_say "I'll auto-pick your project root — usually the repo you're in, or deepiri-platform if we're sitting next to it."
  fi
  if [ "$NO_GLOBAL" -eq 1 ]; then
    axiom_say "Heads up: you passed --no-global. I'll only install into this project — I won't copy myself to ~/.cursor for every workspace. Fine if you want project-scoped only."
  else
    axiom_say "By default I'll also register myself under your user profile (~/.cursor/agents, ~/.gemini) so you can summon me in ${BOLD}any${RESET} folder, not just one repo."
  fi
  printf '\n'
}

axiom_intro_detect() {
  axiom_say "Quick scan mode. I'm Deepiri Axiom — I'll map your ecosystem and write .axiom/ecosystem.json. No full install this time."
  printf '\n'
}

axiom_intro_doctor() {
  axiom_say "Doctor mode. I'm Deepiri Axiom — let me check whether I'm installed correctly and your manifest looks sane."
  printf '\n'
}

axiom_after_detect() {
  local root="${1:-$REPO_ROOT}"
  local manifest="$root/.axiom/ecosystem.json"
  local summary gpu arch wsl repo_count repo_names repo_more prov_count prov_names tools

  summary="$(manifest_summary "$manifest")"
  gpu="$(printf '%s\n' "$summary" | sed -n 's/^GPU://p')"
  arch="$(printf '%s\n' "$summary" | sed -n 's/^ARCH://p')"
  wsl="$(printf '%s\n' "$summary" | sed -n 's/^WSL://p')"
  repo_count="$(printf '%s\n' "$summary" | sed -n 's/^REPOS://p')"
  repo_names="$(printf '%s\n' "$summary" | sed -n 's/^REPO_NAMES://p')"
  repo_more="$(printf '%s\n' "$summary" | sed -n 's/^REPO_MORE://p')"
  prov_count="$(printf '%s\n' "$summary" | sed -n 's/^PROVIDERS://p')"
  prov_names="$(printf '%s\n' "$summary" | sed -n 's/^PROVIDER_NAMES://p')"
  tools="$(printf '%s\n' "$summary" | sed -n 's/^TOOLS://p')"

  axiom_say "Alright — I looked around. Here's what I see on ${BOLD}your${RESET} machine:"
  axiom_pause

  if [ "$gpu" = "yes" ]; then
    axiom_say "You've got an NVIDIA GPU. Good — I can steer you toward local Ollama, zepgpu, gpu-utils, and the heavier ML repos without pretending you're on a Chromebook."
  else
    axiom_say "No NVIDIA GPU detected from here. I'll bias recommendations toward API providers and lighter local inference — still fine for most Deepiri dev work."
  fi

  if [ "$wsl" = "True" ]; then
    axiom_say "You're on WSL. I've been here before — watch path quirks, line endings, and GPU passthrough if you expect CUDA inside Linux."
  fi

  if [ -n "$repo_count" ] && [ "$repo_count" -gt 0 ] 2>/dev/null; then
    local repo_line="I found ${repo_count} Deepiri repo clone(s) near you"
    if [ -n "$repo_names" ]; then
      repo_line="${repo_line}: ${repo_names}"
      [ -n "$repo_more" ] && repo_line="${repo_line} …and ${repo_more} more"
    fi
    repo_line="${repo_line}. I'll use those paths when you ask cross-repo questions — no guessing where deepiri-platform lives."
    axiom_say "$repo_line"
  else
    axiom_say "I don't see sibling deepiri-* or diri-* clones yet. That's OK — I still carry the full org repo map. Clone what you need; re-run ./setup.sh and I'll pick them up."
  fi

  if [ -n "$prov_count" ] && [ "$prov_count" -gt 0 ] 2>/dev/null; then
    axiom_say "Model providers I can see: ${prov_names:-unknown}. I won't ask you to paste API keys — I only check what's already configured."
  else
    axiom_say "No model providers jumped out. If you use Ollama or cloud APIs, set them up and run me again — I'll notice."
  fi

  if [ -n "$tools" ]; then
    axiom_say "For tooling, I'm going to hook into: ${tools}. That's what I detected on your PATH and config dirs."
  fi

  axiom_say "I saved the snapshot to .axiom/ecosystem.json. That's ${BOLD}your${RESET} machine state — gitignored, refresh anytime with ./setup.sh."
  printf '\n'
}

axiom_before_install() {
  axiom_say "Next I'm writing myself into your AI tools — Cursor agent, Claude, Copilot, Gemini, OpenCode, whichever applies."
  axiom_pause
  axiom_say "You'll get prompts with my full Deepiri context: org repo map, your local clones, device/provider hints, and how to behave like a 1-on-1 platform expert."
  printf '\n'
}

axiom_outro_full() {
  axiom_say "I'm installed. Here's how to use me — read this, it's the whole point:"
  axiom_pause
  axiom_say "${BOLD}In Cursor:${RESET} open the agent/subagent menu and pick ${BOLD}deepiri-axiom${RESET} (Deepiri Genius). Restart Cursor if I don't show up. I'm also at .cursor/agents/deepiri-axiom.md in your target repo."
  axiom_say "${BOLD}In Claude Code / Gemini / Copilot / OpenCode:${RESET} my instructions are in the project files this install just wrote — CLAUDE.md, GEMINI.md, .github/copilot-instructions.md, .opencode/, etc."
  axiom_pause
  axiom_say "Ask me things like: \"which repo owns Persola fine-tuning?\", \"trace a request from the gateway to Cyrex\", \"where should this migration live?\", \"what's the blast radius of this change?\""
  axiom_say "I will correct you if you violate service boundaries — no cross-service DB access, auth before expensive work, Prisma migrations only in the owning service. That's not nagging; that's how Deepiri stays shippable."
  axiom_pause
  axiom_say "Re-run ${BOLD}./setup.sh${RESET} whenever you clone new repos, change providers, or switch machines. ${BOLD}python3 setup.py status${RESET} shows my manifest; ${BOLD}python3 setup.py doctor${RESET} if something feels off."
  axiom_pause
  axiom_say "I'm your subagent now. Open your editor, summon me, and let's build."
  printf '\n'
}

axiom_outro_detect() {
  axiom_say "Scan done. Manifest is at .axiom/ecosystem.json. When you're ready for the full install, run ./setup.sh without --detect."
  printf '\n'
}

ensure_python() {
  command -v python3 >/dev/null 2>&1 || die "python3 is required (3.10+)."
  python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)' \
    || die "Python 3.10+ required."
}

detect_target_root() {
  if [ -n "$TARGET" ]; then
    printf '%s' "$TARGET"
    return
  fi
  python3 -c "
from cli.installer import find_default_target
print(find_default_target())
" 2>/dev/null || printf '%s' "$REPO_ROOT"
}

run_detect() {
  local detect_args=(detect --write)
  [ -n "$TARGET" ] && detect_args+=(--target "$TARGET")
  python3 setup.py "${detect_args[@]}" >/dev/null
}

run_install() {
  local install_args=(install --no-spinner)
  [ -n "$TARGET" ] && install_args+=(--target "$TARGET")
  [ "$NO_GLOBAL" -eq 1 ] && install_args+=(--no-global)

  local manifest_root
  manifest_root="$(detect_target_root)"
  local tools=""
  if [ -f "$manifest_root/.axiom/ecosystem.json" ]; then
    tools="$(python3 -c "
import json
from pathlib import Path
p = Path('$manifest_root/.axiom/ecosystem.json')
d = json.loads(p.read_text())
t = d.get('recommended_tools') or []
print(','.join(t) if t else '')
" 2>/dev/null || true)"
  fi
  if [ -n "$tools" ]; then
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

# --- main -------------------------------------------------------------------
ensure_python

if [ "$DOCTOR" -eq 1 ]; then
  axiom_intro_doctor
  run_doctor
  exit $?
fi

if [ "$DETECT_ONLY" -eq 1 ]; then
  axiom_intro_detect
else
  axiom_intro_full
fi

axiom_say "Give me a second — I'm scanning your device, model providers, installed apps, and nearby Deepiri repos..."
info "Scanning ecosystem..."
run_detect
SCAN_ROOT="$(detect_target_root)"
axiom_after_detect "$SCAN_ROOT"

if [ "$DETECT_ONLY" -eq 1 ]; then
  axiom_outro_detect
  exit 0
fi

axiom_before_install
info "Installing into AI tools..."
run_install

axiom_say "Running a quick health check on myself..."
info "Doctor..."
run_doctor || axiom_say "One or more checks failed above — run python3 setup.py doctor for details. I may be partially installed."

axiom_outro_full
