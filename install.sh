#!/usr/bin/env bash
#
# Deepiri Axiom — pure-bash installer (no Python required).
#
# Usage:
#   ./install.sh                         Full bootstrap: detect + install + doctor
#   ./install.sh install [opts]          Install agents/skills into target
#   ./install.sh bootstrap [opts]        Same as install
#   ./install.sh subagent [opts]         Cursor-only, project-scoped
#   ./install.sh list-tools              Show detected AI tools
#   ./install.sh detect [--write]        Scan device / providers / sibling repos
#   ./install.sh link                    Refresh .axiom/ecosystem.json + links
#   ./install.sh doctor                  Health checks
#   ./install.sh status                  Manifest summary
#
# Compat flags (same as legacy setup.sh):
#   --detect  --doctor  --target DIR  --no-global  --help
#
# Install options:
#   --target DIR   Project root (default: cwd git root, or sibling deepiri-control-plane / deepiri-platform)
#   --tools LIST   all | auto | cursor,claude,copilot,gemini,opencode
#   --dry-run      Print actions only
#   --force        Overwrite without .bak
#   --no-global    Skip ~/.cursor and ~/.gemini
#   --with-global  (subagent) also write user-level Cursor agent
#
set -euo pipefail

# ── colors / log ─────────────────────────────────────────────────────────────
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
say()   { printf '%s\n' "$*"; }

# ── paths ────────────────────────────────────────────────────────────────────
REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PROMPTS="$REPO_ROOT/prompts"
TEMPLATES="$REPO_ROOT/templates"
SKILLS_ROOT="$REPO_ROOT/skills"
HOME_DIR="${HOME:-$(eval echo ~)}"

TARGET=""
TOOLS="all"
DRY_RUN=0
FORCE=0
NO_GLOBAL=0
WITH_GLOBAL=0
WRITE_MANIFEST=0
COMMAND=""

# ── help ─────────────────────────────────────────────────────────────────────
usage() {
  sed -n '2,28p' "$0" | sed 's/^# \{0,1\}//'
}

# ── argv ─────────────────────────────────────────────────────────────────────
parse_install_opts() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --target)
        shift
        TARGET="${1:-}"
        [ -n "$TARGET" ] || die "--target requires a path"
        shift
        ;;
      --tools)
        shift
        TOOLS="${1:-}"
        [ -n "$TOOLS" ] || die "--tools requires a value"
        shift
        ;;
      --dry-run) DRY_RUN=1; shift ;;
      --force) FORCE=1; shift ;;
      --no-global) NO_GLOBAL=1; shift ;;
      --with-global) WITH_GLOBAL=1; shift ;;
      --write) WRITE_MANIFEST=1; shift ;;
      --no-spinner) shift ;; # accepted, ignored (bash has no spinner dependency)
      --help|-h) usage; exit 0 ;;
      -*) die "unknown option: $1 (try --help)" ;;
      *) die "unexpected argument: $1" ;;
    esac
  done
}

# First positional may be a subcommand; bare flags keep legacy setup.sh UX.
if [ $# -eq 0 ]; then
  COMMAND="bootstrap-full"
else
  case "$1" in
    install|bootstrap|subagent|list-tools|detect|link|doctor|status)
      COMMAND="$1"
      shift
      parse_install_opts "$@"
      ;;
    --detect) COMMAND="detect"; WRITE_MANIFEST=1; shift; parse_install_opts "$@" ;;
    --doctor) COMMAND="doctor"; shift; parse_install_opts "$@" ;;
    --help|-h) usage; exit 0 ;;
    --target|--tools|--dry-run|--force|--no-global|--with-global|--no-spinner)
      COMMAND="bootstrap-full"
      parse_install_opts "$@"
      ;;
    *)
      # Legacy: flags-only or unknown → treat as install flags
      COMMAND="bootstrap-full"
      parse_install_opts "$@"
      ;;
  esac
fi

# ── helpers ──────────────────────────────────────────────────────────────────
have() { command -v "$1" >/dev/null 2>&1; }

abs_path() {
  local p="$1"
  if [ -d "$p" ]; then (cd "$p" && pwd)
  elif [ -f "$p" ]; then (cd "$(dirname "$p")" && printf '%s/%s\n' "$(pwd)" "$(basename "$p")")
  else printf '%s\n' "$p"
  fi
}

cwd_git_root() {
  local d
  d="$(pwd)"
  while [ "$d" != "/" ]; do
    if [ -d "$d/.git" ] || [ -f "$d/.git" ]; then
      printf '%s\n' "$d"
      return
    fi
    d="$(dirname "$d")"
  done
  pwd
}

find_default_target() {
  if [ -n "$TARGET" ]; then
    abs_path "$TARGET"
    return
  fi
  local cwd axiom_parent sib
  cwd="$(pwd)"
  # Dogfood: when inside axiom source, prefer sibling deepiri-control-plane (else deepiri-platform)
  case "$cwd" in
    "$REPO_ROOT"|"$REPO_ROOT"/*)
      sib="$(dirname "$REPO_ROOT")/deepiri-control-plane"
      if [ ! -d "$sib" ]; then
        sib="$(dirname "$REPO_ROOT")/deepiri-platform"
      fi
      if [ -d "$sib" ]; then
        abs_path "$sib"
        return
      fi
      ;;
  esac
  cwd_git_root
}

backup_if_exists() {
  local path="$1"
  [ -f "$path" ] || return 0
  [ "$FORCE" -eq 1 ] && return 0
  local bak="${path}.bak" n=1
  while [ -e "$bak" ]; do
    bak="${path}.bak.${n}"
    n=$((n + 1))
  done
  cp -a "$path" "$bak"
  say "  (backup: $bak)"
}

write_file() {
  local path="$1"
  local src="$2"   # file containing content
  mkdir -p "$(dirname "$path")"
  if [ "$DRY_RUN" -eq 1 ]; then
    say "  [dry-run] would write $path ($(wc -c < "$src" | tr -d ' ') bytes)"
    return
  fi
  if [ -e "$path" ]; then
    backup_if_exists "$path"
  fi
  cp -a "$src" "$path"
  say "  wrote $path"
}

write_file_if_absent() {
  local path="$1"
  local src="$2"
  if [ -e "$path" ]; then
    return 0
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    say "  [dry-run] would write $path (only if missing)"
    return
  fi
  mkdir -p "$(dirname "$path")"
  cp -a "$src" "$path"
  say "  wrote $path (new)"
}

# Copy JSON template: merge fill-missing with jq when present; else write if missing / --force
write_json_template() {
  local dest="$1"
  local template="$2"
  local mode="${3:-fill}" # fill | mcp | claude

  if [ "$DRY_RUN" -eq 1 ]; then
    say "  [dry-run] would write/merge $dest"
    return
  fi
  mkdir -p "$(dirname "$dest")"

  if [ ! -f "$dest" ] || [ "$FORCE" -eq 1 ]; then
    [ -f "$dest" ] && backup_if_exists "$dest"
    cp -a "$template" "$dest"
    say "  wrote $dest"
    return
  fi

  if ! have jq; then
    warn "jq not found — leaving existing $dest unchanged (install jq or pass --force)"
    return
  fi

  local tmp
  tmp="$(mktemp)"
  case "$mode" in
    mcp)
      jq -s '
        .[0] as $e | .[1] as $d |
        (($e // {}) | .mcpServers //= {}) as $ex |
        reduce (($d.mcpServers // {}) | keys[]) as $k ($ex;
          if (.mcpServers | has($k) | not) then .mcpServers[$k] = $d.mcpServers[$k] else . end
        ) |
        reduce (($d | del(.mcpServers) | keys[]) ) as $k (.;
          if (has($k) | not) then .[$k] = $d[$k] else . end
        )
      ' "$dest" "$template" > "$tmp"
      ;;
    claude)
      jq -s '
        .[0] as $e | .[1] as $d |
        ($e // {}) as $ex |
        reduce ($d | keys[]) as $k ($ex;
          if $k == "permissions" then
            .permissions = (.permissions // {}) |
            .permissions.allow = (((.permissions.allow // []) + ($d.permissions.allow // [])) | unique | sort) |
            reduce ((($d.permissions // {}) | keys[]) | map(select(. != "allow"))[]) as $pk (.;
              if (.permissions | has($pk) | not) then .permissions[$pk] = $d.permissions[$pk] else . end)
          elif (has($k) | not) then
            .[$k] = $d[$k]
          else . end
        )
      ' "$dest" "$template" > "$tmp"
      ;;
    *)
      jq -s '
        def deep_fill(a; b):
          if (a|type) == "object" and (b|type) == "object" then
            reduce (b|keys[]) as $k (a;
              if has($k) then .[$k] = deep_fill(.[$k]; b[$k]) else .[$k] = b[$k] end)
          else a end;
        deep_fill(.[0] // {}; .[1] // {})
      ' "$dest" "$template" > "$tmp"
      ;;
  esac

  backup_if_exists "$dest"
  mv "$tmp" "$dest"
  say "  merged $dest"
}

# ── template render (no Python) ──────────────────────────────────────────────
# Placeholders: {{DEEPIRI_CONTEXT}} {{AXIOM_CORE}} {{AXIOM_CONDENSED}}
#               {{COPILOT_BRIEF}} {{AXIOM_BRANCH_TOOLS}}
#               {{TARGET_REPO_CARTOGRAPHY}} {{ECOSYSTEM_CONTEXT}}
MAP_DIR=""

init_map_dir() {
  MAP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/axiom-map.XXXXXX")"
  trap 'rm -rf "$MAP_DIR"' EXIT
}

set_map() {
  local key="$1"
  local file="$2"
  cp -a "$file" "$MAP_DIR/$key"
}

set_map_text() {
  local key="$1"
  printf '%s' "$2" > "$MAP_DIR/$key"
}

render_template() {
  local template="$1"
  local outfile="$2"
  awk -v mapdir="$MAP_DIR" '
    function load(key,   f, line, s, n) {
      f = mapdir "/" key
      s = ""
      n = 0
      while ((getline line < f) > 0) {
        if (n++) s = s "\n"
        s = s line
      }
      close(f)
      return s
    }
    {
      line = $0
      while (match(line, /\{\{[A-Z0-9_]+\}\}/)) {
        key = substr(line, RSTART + 2, RLENGTH - 4)
        repl = load(key)
        line = substr(line, 1, RSTART - 1) repl substr(line, RSTART + RLENGTH)
      }
      print line
    }
  ' "$template" > "$outfile"
}

# ── cartography / ecosystem (lightweight, bash) ──────────────────────────────
build_cartography() {
  local target="$1"
  local out="$2"
  {
    echo "## Target repo snapshot (install-time)"
    echo ""
    echo "*Generated by deepiri-axiom \`./install.sh\`. Re-run \`./install.sh install --target .\` to refresh.*"
    echo ""
    echo "- **Root:** \`$target\`"
    if [ -f "$target/docs/DOCUMENTATION_INDEX.md" ]; then
      echo "- **Docs index:** \`docs/DOCUMENTATION_INDEX.md\` present"
    fi
    if [ -f "$target/README.md" ]; then
      echo "- **README:** present"
    fi
    if [ -f "$target/package.json" ]; then
      echo "- **package.json:** present"
    fi
    if [ -f "$target/pyproject.toml" ]; then
      echo "- **pyproject.toml:** present"
    fi
    if [ -f "$target/docker-compose.yml" ] || [ -f "$target/docker-compose.yaml" ] || [ -f "$target/compose.yml" ]; then
      echo "- **Compose:** present"
    fi
    if [ -f "$target/.gitmodules" ]; then
      echo "- **Submodules:**"
      sed -n 's/^\[submodule "\(.*\)"\]/  - \1/p; s/^[[:space:]]*path = /    path: /p' "$target/.gitmodules" | head -40
    fi
    echo ""
    echo "### Top-level entries"
    echo ""
    ls -1 "$target" 2>/dev/null | head -60 | while read -r name; do
      if [ -d "$target/$name" ]; then
        echo "- \`$name/\`"
      else
        echo "- \`$name\`"
      fi
    done
  } > "$out"
}

global_cartography() {
  local out="$1"
  cat > "$out" <<'EOF'
## Target repo snapshot (user-level install)

Omitted: embedding a per-repo tree would go stale in other workspaces.
For a fresh layout, run `./install.sh subagent` (or `./install.sh install --target <repo> --tools cursor`) from that repository.

This file still includes **AXIOM core** and **Deepiri context** in any folder.
EOF
}

build_ecosystem_context() {
  local target="$1"
  local out="$2"
  local manifest="$target/.axiom/ecosystem.json"
  local parent sibling_list=""
  parent="$(dirname "$target")"

  {
    echo "## Ecosystem context (live)"
    echo ""
    if [ -f "$manifest" ] && have jq; then
      echo "### Manifest"
      echo ""
      echo "- Generated: \`$(jq -r '.generated_at // "unknown"' "$manifest")\`"
      echo "- Repos: $(jq '.repos | length' "$manifest")"
      echo "- Providers available: $(jq '[.providers[]? | select(.available==true)] | length' "$manifest")"
      echo "- Recommended tools: $(jq -r '(.recommended_tools // []) | join(", ")' "$manifest")"
      echo ""
    fi
    echo "### Sibling Deepiri clones near \`$parent\`"
    echo ""
    if [ -d "$parent" ]; then
      for d in "$parent"/deepiri-* "$parent"/diri-*; do
        [ -d "$d" ] || continue
        echo "- \`$(basename "$d")\` — \`$d\`"
      done
    fi
    echo ""
    echo "### Device"
    echo ""
    if have nvidia-smi && nvidia-smi -L >/dev/null 2>&1; then
      echo "- NVIDIA GPU: yes"
    else
      echo "- NVIDIA GPU: no / not detected"
    fi
    echo "- Arch: $(uname -m)"
    if grep -qi microsoft /proc/version 2>/dev/null; then
      echo "- WSL: yes"
    else
      echo "- WSL: no"
    fi
    echo ""
    echo "### Providers (PATH / env hints)"
    echo ""
    have ollama && echo "- ollama: available" || echo "- ollama: not on PATH"
    [ -n "${OPENAI_API_KEY:-}" ] && echo "- OPENAI_API_KEY: set" || echo "- OPENAI_API_KEY: unset"
    [ -n "${ANTHROPIC_API_KEY:-}" ] && echo "- ANTHROPIC_API_KEY: set" || echo "- ANTHROPIC_API_KEY: unset"
    [ -n "${GOOGLE_API_KEY:-}" ] && echo "- GOOGLE_API_KEY: set" || echo "- GOOGLE_API_KEY: unset"
    [ -n "${GEMINI_API_KEY:-}" ] && echo "- GEMINI_API_KEY: set" || echo "- GEMINI_API_KEY: unset"
  } > "$out"
}

# ── tool detection ───────────────────────────────────────────────────────────
tool_cursor=1
tool_claude=0
tool_copilot=1
tool_gemini=0
tool_opencode=0

detect_tools() {
  tool_cursor=1
  tool_copilot=1
  have claude && tool_claude=1 || tool_claude=0
  have gemini && tool_gemini=1 || tool_gemini=0
  have opencode && tool_opencode=1 || tool_opencode=0
}

parse_tools() {
  local arg="${1:-all}"
  local a
  a="$(printf '%s' "$arg" | tr '[:upper:]' '[:lower:]' | tr -d ' ')"
  TOOLS_SET=""
  case "$a" in
    all|"")
      TOOLS_SET="cursor claude copilot gemini opencode"
      ;;
    auto)
      TOOLS_SET="cursor claude copilot gemini"
      [ "$tool_opencode" -eq 1 ] && TOOLS_SET="$TOOLS_SET opencode"
      ;;
    *)
      local IFS=','
      # shellcheck disable=SC2086
      set -- ${a}
      for p in "$@"; do
        case "$p" in
          cursor|claude|copilot|gemini|opencode) TOOLS_SET="$TOOLS_SET $p" ;;
          *) die "Unknown tool: $p. Use: cursor,claude,copilot,gemini,opencode,all,auto" ;;
        esac
      done
      ;;
  esac
}

has_tool() {
  case " $TOOLS_SET " in
    *" $1 "*) return 0 ;;
    *) return 1 ;;
  esac
}

# ── mapping bootstrap ────────────────────────────────────────────────────────
prepare_mapping() {
  local target="$1"
  local mode="${2:-project}" # project | user

  init_map_dir
  set_map DEEPIRI_CONTEXT "$PROMPTS/deepiri-context.md"
  set_map AXIOM_CORE "$PROMPTS/axiom-core.md"
  set_map AXIOM_CONDENSED "$PROMPTS/axiom-condensed.md"
  set_map COPILOT_BRIEF "$PROMPTS/copilot-brief.md"
  set_map AXIOM_BRANCH_TOOLS "$PROMPTS/axiom-branch-tools.md"

  local cart eco
  cart="$(mktemp)"
  eco="$(mktemp)"
  if [ "$mode" = "user" ]; then
    global_cartography "$cart"
  else
    build_cartography "$target" "$cart"
  fi
  build_ecosystem_context "$target" "$eco"
  set_map TARGET_REPO_CARTOGRAPHY "$cart"
  set_map ECOSYSTEM_CONTEXT "$eco"
  rm -f "$cart" "$eco"
}

# ── skills ───────────────────────────────────────────────────────────────────
list_skill_dirs() {
  [ -d "$SKILLS_ROOT" ] || return 0
  for d in "$SKILLS_ROOT"/*/; do
    [ -d "$d" ] || continue
    local name
    name="$(basename "$d")"
    case "$name" in
      .*|_* ) continue ;;
    esac
    if [ -f "$d/SKILL.md" ] || [ -f "$d/SKILL.md.j2" ]; then
      printf '%s\n' "$name"
    fi
  done | sort
}

skill_body_to() {
  local name="$1"
  local out="$2"
  local dir="$SKILLS_ROOT/$name"
  if [ -f "$dir/SKILL.md.j2" ]; then
    render_template "$dir/SKILL.md.j2" "$out"
  elif [ -f "$dir/SKILL.md" ]; then
    cp -a "$dir/SKILL.md" "$out"
  else
    die "No SKILL.md for $name"
  fi
}

install_skills_project() {
  local target="$1"
  local name tmp
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    tmp="$(mktemp)"
    skill_body_to "$name" "$tmp"
    if has_tool cursor; then
      write_file "$target/.cursor/skills/$name/SKILL.md" "$tmp"
    fi
    if has_tool claude; then
      write_file "$target/.claude/skills/$name/SKILL.md" "$tmp"
    fi
    rm -f "$tmp"
  done < <(list_skill_dirs)
}

install_skills_global() {
  local name tmp dest
  while IFS= read -r name; do
    [ -n "$name" ] || continue
    tmp="$(mktemp)"
    skill_body_to "$name" "$tmp"
    dest="$HOME_DIR/.cursor/skills/$name/SKILL.md"
    write_file "$dest" "$tmp"
    rm -f "$tmp"
  done < <(list_skill_dirs)
}

# ── install core ─────────────────────────────────────────────────────────────
cmd_list_tools() {
  detect_tools
  say "Detected (optional: install uses --tools auto to skip OpenCode when missing):"
  say "  cursor: true"
  say "  claude: $([ "$tool_claude" -eq 1 ] && echo true || echo false)"
  say "  copilot: true"
  say "  gemini: $([ "$tool_gemini" -eq 1 ] && echo true || echo false)"
  say "  opencode: $([ "$tool_opencode" -eq 1 ] && echo true || echo false)"
}

cmd_install() {
  local target preset="${1:-full}"
  target="$(find_default_target)"
  detect_tools

  if [ "$preset" = "subagent" ]; then
    TOOLS="cursor"
    NO_GLOBAL=1
    [ "$WITH_GLOBAL" -eq 1 ] && NO_GLOBAL=0
  fi

  parse_tools "$TOOLS"
  prepare_mapping "$target" project

  say "Target: $target"
  say "Tools:$(printf ' %s' $TOOLS_SET)"
  say ""

  local tmp

  if has_tool cursor; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/cursor/agent.md.j2" "$tmp"
    write_file "$target/.cursor/agents/deepiri-axiom.md" "$tmp"
    render_template "$TEMPLATES/cursor/rules-deepiri-axiom.md.j2" "$tmp"
    write_file "$target/.cursor/rules/deepiri-axiom.mdc" "$tmp"
    rm -f "$tmp"
  fi

  if has_tool claude; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/claude.md.j2" "$tmp"
    write_file "$target/CLAUDE.md" "$tmp"
    render_template "$TEMPLATES/claude/CLAUDE.local.md.j2" "$tmp"
    write_file "$target/CLAUDE.local.md" "$tmp"
    render_template "$TEMPLATES/claude/agent.md.j2" "$tmp"
    write_file "$target/.claude/agents/deepiri-axiom.md" "$tmp"
    render_template "$TEMPLATES/claude/rules.md.j2" "$tmp"
    write_file "$target/.claude/rules/deepiri-axiom.md" "$tmp"
    write_file "$target/.claude/commands/axiom.md" "$TEMPLATES/claude/command-axiom.md"
    rm -f "$tmp"
  fi

  if has_tool cursor || has_tool claude; then
    install_skills_project "$target"
  fi

  if has_tool copilot; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/copilot/copilot-instructions.md.j2" "$tmp"
    write_file "$target/.github/copilot-instructions.md" "$tmp"
    render_template "$TEMPLATES/copilot/instructions-deepiri-axiom.instructions.md.j2" "$tmp"
    write_file "$target/.github/instructions/deepiri-axiom.instructions.md" "$tmp"
    rm -f "$tmp"
  fi

  if has_tool gemini; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/gemini/GEMINI.md.j2" "$tmp"
    write_file "$target/GEMINI.md" "$tmp"
    rm -f "$tmp"
  fi

  if has_tool opencode; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/opencode/instructions.md.j2" "$tmp"
    write_file "$target/.opencode/instructions.md" "$tmp"
    render_template "$TEMPLATES/opencode/agents/deepiri-axiom.md.j2" "$tmp"
    write_file "$target/.opencode/agents/deepiri-axiom.md" "$tmp"
    write_file "$target/.opencode/commands/axiom.md" "$TEMPLATES/opencode/commands/axiom.md"
    rm -f "$tmp"
  fi

  if has_tool cursor; then
    write_json_template "$target/.cursor/mcp.json" "$TEMPLATES/cursor/mcp.json" mcp
    write_file_if_absent "$target/.cursorignore" "$TEMPLATES/cursor/cursorignore"
    write_file_if_absent "$target/AGENTS.md" "$TEMPLATES/cursor/AGENTS.md"
  fi

  if has_tool claude; then
    write_json_template "$target/.claude/settings.json" "$TEMPLATES/claude/settings.json" claude
    write_json_template "$target/.claude/settings.local.json" "$TEMPLATES/claude/settings.local.json" claude
  fi

  if has_tool gemini; then
    write_json_template "$target/.gemini/settings.json" "$TEMPLATES/gemini/settings.json" fill
    write_file_if_absent "$target/.geminiignore" "$TEMPLATES/gemini/geminiignore"
  fi

  if has_tool opencode; then
    write_json_template "$target/opencode.json" "$TEMPLATES/opencode/opencode.json" fill
  fi

  if [ "$NO_GLOBAL" -eq 0 ]; then
    cmd_global_install "$target"
  fi

  if [ "$preset" = "subagent" ] && has_tool cursor; then
    say ""
    say "Cursor: open the **subagent / custom agent** menu and run **deepiri-axiom** (Deepiri Genius)."
    say "  If it does not appear, restart Cursor; project file is at .cursor/agents/deepiri-axiom.md"
    [ "$NO_GLOBAL" -eq 1 ] && say "  (Project-only install — no user-level copy under ~/.cursor)"
  fi

  if { has_tool cursor || has_tool claude; } && [ "$DRY_RUN" -eq 0 ]; then
    local n
    n="$(list_skill_dirs | wc -l | tr -d ' ')"
    say ""
    say "Skills: installed $n skill(s) to project .cursor/skills/ and/or .claude/skills/ (see skills/README.md)."
  fi

  say "Done."
}

cmd_global_install() {
  local target="$1"
  prepare_mapping "$target" user

  say ""
  say "User-level (available in any project / workspace):"

  local tmp
  if has_tool cursor; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/cursor/agent.md.j2" "$tmp"
    write_file "$HOME_DIR/.cursor/agents/deepiri-axiom.md" "$tmp"
    rm -f "$tmp"
    install_skills_global
  fi

  if has_tool gemini; then
    tmp="$(mktemp)"
    render_template "$TEMPLATES/gemini/GEMINI.md.j2" "$tmp"
    write_file "$HOME_DIR/.gemini/deepiri-axiom.md" "$tmp"
    rm -f "$tmp"
    if [ "$DRY_RUN" -eq 0 ]; then
      local gem="$HOME_DIR/.gemini/GEMINI.md"
      if [ ! -f "$gem" ]; then
        mkdir -p "$(dirname "$gem")"
        cat > "$gem" <<EOF
# Global Gemini context (deepiri-axiom)

<!-- deepiri-axiom-context -->
Full Deepiri AXIOM instructions are in:
  $HOME_DIR/.gemini/deepiri-axiom.md

If your Gemini CLI supports \`@file\` or includes, reference that path;
otherwise merge the sections you need into this file.
EOF
        say "  created $gem (stub pointing at deepiri-axiom context)"
      else
        say "  Gemini: optional — merge or @-include $HOME_DIR/.gemini/deepiri-axiom.md into $gem"
      fi
    fi
  fi

  if has_tool cursor && [ "$DRY_RUN" -eq 0 ]; then
    say ""
    say "Cursor: open any folder — Agent list should include **deepiri-axiom** ($HOME_DIR/.cursor/agents/deepiri-axiom.md). Restart Cursor if it does not appear."
  fi
}

# ── detect / link / status / doctor ──────────────────────────────────────────
write_ecosystem_manifest() {
  local target="$1"
  local out="$target/.axiom/ecosystem.json"
  mkdir -p "$target/.axiom"

  local parent arch gpu=false wsl=false
  parent="$(dirname "$target")"
  arch="$(uname -m)"
  if have nvidia-smi && nvidia-smi -L >/dev/null 2>&1; then gpu=true; fi
  if grep -qi microsoft /proc/version 2>/dev/null; then wsl=true; fi

  local generated
  generated="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

  if have jq; then
    local repos_json='[]' providers_json='[]' apps_json='[]' tools_json='["cursor","copilot"]'
    local rjson='[]'

    # repos
    if [ -d "$parent" ]; then
      rjson='[]'
      for d in "$parent"/deepiri-* "$parent"/diri-*; do
        [ -d "$d" ] || continue
        local name path has_git remote
        name="$(basename "$d")"
        path="$(abs_path "$d")"
        has_git=false
        [ -e "$d/.git" ] && has_git=true
        remote=""
        if [ "$has_git" = true ]; then
          remote="$(git -C "$d" remote get-url origin 2>/dev/null || true)"
        fi
        rjson="$(jq -c --arg n "$name" --arg p "$path" --argjson g "$has_git" --arg r "$remote" \
          '. + [{name:$n, path:$p, has_git:$g, remote_url:$r, discovery:"sibling"}]' <<<"$rjson")"
      done
      repos_json="$rjson"
    fi

    # providers
    providers_json='[]'
    if have ollama; then
      providers_json="$(jq -c '. + [{name:"ollama", available:true}]' <<<"$providers_json")"
    else
      providers_json="$(jq -c '. + [{name:"ollama", available:false}]' <<<"$providers_json")"
    fi
    for key in OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY; do
      if [ -n "${!key:-}" ]; then
        providers_json="$(jq -c --arg n "$key" '. + [{name:$n, available:true}]' <<<"$providers_json")"
      fi
    done

    # apps / recommended tools
    detect_tools
    tools_json='["cursor","copilot"]'
    [ "$tool_claude" -eq 1 ] && tools_json="$(jq -c '. + ["claude"]' <<<"$tools_json")"
    [ "$tool_gemini" -eq 1 ] && tools_json="$(jq -c '. + ["gemini"]' <<<"$tools_json")"
    [ "$tool_opencode" -eq 1 ] && tools_json="$(jq -c '. + ["opencode"]' <<<"$tools_json")"

    jq -n \
      --arg gen "$generated" \
      --arg arch "$arch" \
      --argjson gpu "$gpu" \
      --argjson wsl "$wsl" \
      --argjson repos "$repos_json" \
      --argjson providers "$providers_json" \
      --argjson tools "$tools_json" \
      '{
        generated_at: $gen,
        device: {arch: $arch, has_nvidia_gpu: $gpu, is_wsl: $wsl},
        providers: $providers,
        apps: [],
        repos: $repos,
        links: [],
        recommended_tools: $tools
      }' > "$out"
  else
    # Minimal JSON without jq
    cat > "$out" <<EOF
{
  "generated_at": "$generated",
  "device": {"arch": "$arch", "has_nvidia_gpu": $gpu, "is_wsl": $wsl},
  "providers": [],
  "apps": [],
  "repos": [],
  "links": [],
  "recommended_tools": ["cursor", "claude", "copilot", "gemini"]
}
EOF
  fi
  say "Wrote $out"
}

cmd_detect() {
  local target
  target="$(find_default_target)"
  say "Ecosystem scan @ $target"
  if [ "$WRITE_MANIFEST" -eq 1 ] || [ "$COMMAND" = "link" ]; then
    write_ecosystem_manifest "$target"
  else
    # Print a readable summary without requiring write
    WRITE_MANIFEST=1
    write_ecosystem_manifest "$target"
  fi
  if have jq && [ -f "$target/.axiom/ecosystem.json" ]; then
    jq . "$target/.axiom/ecosystem.json"
  fi
}

cmd_link() {
  WRITE_MANIFEST=1
  cmd_detect
  local target
  target="$(find_default_target)"
  if have jq && [ -f "$target/.axiom/ecosystem.json" ]; then
    local nrepos nlinks
    nrepos="$(jq '.repos | length' "$target/.axiom/ecosystem.json")"
    nlinks="$(jq '.links | length' "$target/.axiom/ecosystem.json")"
    say "Linked $nlinks relationship(s) across $nrepos repo(s)."
    say "Manifest: $target/.axiom/ecosystem.json"
  fi
}

cmd_status() {
  local target manifest
  target="$(find_default_target)"
  manifest="$target/.axiom/ecosystem.json"
  if [ ! -f "$manifest" ]; then
    say "No manifest at $manifest — run ./install.sh detect --write"
    return 1
  fi
  say "Status @ $target"
  if have jq; then
    say "  generated: $(jq -r '.generated_at // "?"' "$manifest")"
    say "  repos: $(jq '.repos | length' "$manifest")"
    say "  providers (available): $(jq '[.providers[]? | select(.available==true)] | length' "$manifest")"
    say "  links: $(jq '.links | length' "$manifest")"
    say "  recommended_tools: $(jq -r '(.recommended_tools // []) | join(", ")' "$manifest")"
  else
    say "  manifest: $manifest (install jq for a detailed summary)"
  fi
}

cmd_doctor() {
  local target fail=0
  target="$(find_default_target)"
  say "Doctor @ $target"
  say ""

  check() {
    local name="$1" ok="$2" msg="$3"
    if [ "$ok" -eq 1 ]; then
      say "  [OK] $name: $msg"
    else
      say "  [FAIL] $name: $msg"
      fail=1
    fi
  }

  if [ -f "$target/.axiom/ecosystem.json" ]; then
    check "manifest" 1 "present at .axiom/ecosystem.json"
  else
    check "manifest" 0 "missing — run ./install.sh detect --write"
  fi

  if [ -f "$target/.cursor/agents/deepiri-axiom.md" ] || [ -f "$HOME_DIR/.cursor/agents/deepiri-axiom.md" ]; then
    check "cursor-agent" 1 "deepiri-axiom agent installed"
  else
    check "cursor-agent" 0 "not installed — run ./install.sh"
  fi

  if [ -d "$REPO_ROOT/skills" ]; then
    check "skills-pack" 1 "$(list_skill_dirs | wc -l | tr -d ' ') packaged skills in repo"
  else
    check "skills-pack" 0 "skills/ missing from axiom checkout"
  fi

  if [ -f "$PROMPTS/deepiri-context.md" ] && [ -f "$PROMPTS/axiom-core.md" ]; then
    check "prompts" 1 "core prompts present"
  else
    check "prompts" 0 "prompts/ incomplete"
  fi

  return "$fail"
}

# ── full bootstrap (legacy setup.sh voice, optional) ─────────────────────────
cmd_bootstrap_full() {
  local target
  target="$(find_default_target)"
  info "Scanning ecosystem..."
  WRITE_MANIFEST=1
  write_ecosystem_manifest "$target" >/dev/null
  say "Manifest: $target/.axiom/ecosystem.json"

  # Prefer recommended tools from manifest when --tools still default all
  if [ "$TOOLS" = "all" ] && have jq && [ -f "$target/.axiom/ecosystem.json" ]; then
    local rec
    rec="$(jq -r '(.recommended_tools // []) | join(",")' "$target/.axiom/ecosystem.json")"
    if [ -n "$rec" ]; then
      TOOLS="$rec"
    fi
  fi

  info "Installing into AI tools..."
  cmd_install full

  info "Doctor..."
  cmd_doctor || warn "One or more checks failed — run ./install.sh doctor for details."
}

# ── main ─────────────────────────────────────────────────────────────────────
cd "$REPO_ROOT"

case "$COMMAND" in
  bootstrap-full) cmd_bootstrap_full ;;
  install|bootstrap) cmd_install full ;;
  subagent) cmd_install subagent ;;
  list-tools) cmd_list_tools ;;
  detect) cmd_detect ;;
  link) cmd_link ;;
  doctor) cmd_doctor ;;
  status) cmd_status ;;
  *) die "unknown command: $COMMAND" ;;
esac
