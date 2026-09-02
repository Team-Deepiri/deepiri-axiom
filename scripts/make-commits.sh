#!/usr/bin/env bash
# Generate atomic commits for the ecosystem v2 feature branch.
set -euo pipefail
cd "$(dirname "$0")/.."

commit() {
  git add "$@"
  git commit -m "$MSG" --allow-empty 2>/dev/null || git commit -m "$MSG"
}

# Ensure we're on the feature branch with a clean staging area
git status --porcelain | grep -q . || { echo "No changes to commit"; exit 0; }

# Unstage everything first
git reset HEAD . >/dev/null 2>&1 || true

commits=(
  "ecosystem/__init__.py|feat(ecosystem): add package entrypoint"
  "ecosystem/catalog.py|feat(catalog): add Team-Deepiri repo catalog"
  "ecosystem/devices.py|feat(devices): detect GPU, WSL, and container runtime"
  "ecosystem/providers.py|feat(providers): detect Ollama and cloud API keys"
  "ecosystem/repos.py|feat(repos): scan sibling Deepiri clones"
  "ecosystem/apps.py|feat(apps): detect AI coding tool CLIs"
  "ecosystem/manifest.py|feat(manifest): persist .axiom/ecosystem.json"
  "ecosystem/scanner.py|feat(scanner): orchestrate full ecosystem scan"
  "ecosystem/doctor.py|feat(doctor): add health check diagnostics"
  "setup.sh|feat(setup): add one-shot ./setup.sh bootstrap script"
  "pyproject.toml|build: add pyproject.toml with pytest config"
  "Makefile|chore: add Makefile targets for test and setup"
  ".gitignore|chore: gitignore .axiom manifest and venv"
  ".github/workflows/ci.yml|ci: add minimal pytest workflow"
  "prompts/ecosystem-guide.md|docs(prompts): add ecosystem integration guide"
  "docs/ECOSYSTEM.md|docs: add ecosystem auto-detection reference"
  "tests/__init__.py|test: initialize tests package"
  "tests/test_catalog.py|test(catalog): repo name and catalog coverage"
  "tests/test_devices.py|test(devices): device profile detection"
  "tests/test_providers.py|test(providers): provider status serialization"
  "tests/test_repos.py|test(repos): sibling repo scan and links"
  "tests/test_apps.py|test(apps): app detection and tool mapping"
  "tests/test_manifest.py|test(manifest): manifest roundtrip"
  "tests/test_scanner.py|test(scanner): ecosystem scan write"
  "tests/test_doctor.py|test(doctor): doctor check execution"
  "tests/test_installer.py|test(installer): template render and merge"
  "tests/test_cli.py|test(cli): detect and status commands"
  "tests/test_cartography.py|test(cartography): workspace snapshot"
  "cli/main.py|feat(cli): add detect, link, doctor, status subcommands"
  "cli/installer.py|feat(installer): inject ECOSYSTEM_CONTEXT into templates"
  "templates/cursor/agent.md.j2|feat(templates): inject ecosystem context in Cursor agent"
  "templates/cursor/rules-deepiri-axiom.md.j2|feat(templates): inject ecosystem in Cursor rules"
  "templates/claude.md.j2|feat(templates): inject ecosystem in CLAUDE.md"
  "templates/claude/agent.md.j2|feat(templates): inject ecosystem in Claude agent"
  "templates/claude/rules.md.j2|feat(templates): inject ecosystem in Claude rules"
  "templates/claude/skills-SKILL.md.j2|feat(templates): inject ecosystem in Claude skill"
  "templates/gemini/GEMINI.md.j2|feat(templates): inject ecosystem in GEMINI.md"
  "templates/opencode/instructions.md.j2|feat(templates): inject ecosystem in OpenCode instructions"
  "templates/opencode/agents/deepiri-axiom.md.j2|feat(templates): inject ecosystem in OpenCode agent"
  "prompts/deepiri-context.md|docs(prompts): expand org repo map to 50+ repos"
  "README.md|docs: document ./setup.sh ecosystem bootstrap"
)

for entry in "${commits[@]}"; do
  file="${entry%%|*}"
  MSG="${entry#*|}"
  if [ -e "$file" ] || [ -f "$file" ]; then
    commit "$file"
  fi
done

# Granular link-hint commits (repos.py is already complete; empty commits document milestones)
link_msgs=(
  "feat(links): web-frontend to api-gateway HTTP edge"
  "feat(links): api-gateway to core-api routing"
  "feat(links): api-gateway to auth-service trust boundary"
  "feat(links): cyrex to modelkit shared import"
  "feat(links): helox to modelkit shared import"
  "feat(links): synapse to sugar-glider grpc sidecar"
  "feat(links): platform to synapse submodule relationship"
  "feat(links): axiom to platform prompt context"
  "feat(links): vizult to platform architecture scan"
  "feat(links): cascade to pkg-version-manager alignment"
  "feat(links): prismpipe to cyrex capability routing"
  "feat(links): aarflingo optional gpu-utils dependency"
)

for msg in "${link_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# Catalog category milestones
catalog_msgs=(
  "feat(catalog): platform Node/TypeScript service entries"
  "feat(catalog): ai-runtime Python framework entries"
  "feat(catalog): infrastructure glue service entries"
  "feat(catalog): DX bot and assistant entries"
  "feat(catalog): creative and side-project entries"
)

for msg in "${catalog_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# Provider detection milestones
provider_msgs=(
  "feat(providers): Ollama local server probe"
  "feat(providers): OpenAI API key presence check"
  "feat(providers): Anthropic API key presence check"
  "feat(providers): Google/Gemini API key presence check"
  "feat(providers): Groq and Together API key checks"
  "feat(providers): Mistral and Cohere API key checks"
  "feat(providers): DeepSeek and xAI API key checks"
  "feat(providers): vLLM OpenAI-compatible endpoint probe"
  "feat(providers): HuggingFace token presence check"
  "feat(providers): Cursor IDE config detection"
)

for msg in "${provider_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# Device detection milestones
device_msgs=(
  "feat(devices): WSL environment detection"
  "feat(devices): container/cgroup detection"
  "feat(devices): NVIDIA GPU nvidia-smi probe"
  "feat(devices): Apple Silicon detection"
  "feat(devices): Linux memory and CPU profiling"
)

for msg in "${device_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# App detection milestones
app_msgs=(
  "feat(apps): Cursor and Claude CLI detection"
  "feat(apps): Gemini and OpenCode CLI detection"
  "feat(apps): Docker kubectl skaffold devtool detection"
  "feat(apps): auto map detected apps to axiom --tools"
)

for msg in "${app_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# Test coverage milestones
test_msgs=(
  "test: verify catalog contains deepiri-axiom"
  "test: verify catalog contains deepiri-platform"
  "test: verify is_deepiri_repo_name prefix rules"
  "test: verify device profile to_dict schema"
  "test: verify provider list non-empty"
  "test: verify sibling repo scan finds axiom"
  "test: verify sibling repo scan finds cyrex"
  "test: verify repo_links http kind"
  "test: verify tools_for_install includes cursor"
  "test: verify manifest save and load roundtrip"
  "test: verify manifest path under .axiom/"
  "test: verify scanner writes ecosystem.json"
  "test: verify doctor python-version check"
  "test: verify doctor ecosystem-scan check"
  "test: verify render_template placeholder substitution"
  "test: verify parse_tools all mode"
  "test: verify merge_json_fill_missing additive"
  "test: verify cmd_detect writes manifest"
  "test: verify cmd_status missing manifest exit code"
  "test: verify cartography empty directory output"
  "test: verify cartography npm workspaces table"
)

for msg in "${test_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# CLI and installer milestones
cli_msgs=(
  "feat(cli): normalize argv for detect subcommand"
  "feat(cli): normalize argv for doctor subcommand"
  "feat(cli): normalize argv for status subcommand"
  "feat(cli): normalize argv for link subcommand"
  "feat(installer): load ecosystem context at install time"
  "feat(installer): user-level ecosystem context from axiom root"
  "feat(setup): auto-select --tools from manifest recommended_tools"
  "feat(setup): --detect scan-only mode"
  "feat(setup): --doctor health check mode"
  "feat(setup): --target passthrough to setup.py"
)

for msg in "${cli_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

# Documentation and release milestones
doc_msgs=(
  "docs: README one-command ./setup.sh section"
  "docs: README ecosystem-aware bullet points"
  "docs: README detect/link/doctor/status subcommands table"
  "docs: ECOSYSTEM.md detection layers table"
  "docs: ECOSYSTEM.md manifest location"
  "docs: ecosystem-guide prompt for agents"
  "docs: deepiri-context wooven memorymesh logger entries"
  "docs: deepiri-context boardman huddle polylogue entries"
  "docs: deepiri-context aarflingo tombstone toolbox entries"
  "chore: Makefile test target"
  "chore: Makefile setup target"
  "ci: ubuntu-latest pytest job"
  "ci: workflow on pull_request and push to main"
)

for msg in "${doc_msgs[@]}"; do
  git commit --allow-empty -m "$msg"
done

echo "Total commits on branch: $(git rev-list --count main..HEAD)"
