#!/usr/bin/env bash
# Install Copy Studio, the five skills it calls, and the /copy-studio slash command.
#
#   curl -fsSL https://raw.githubusercontent.com/Ekko237/copy-studio/main/install.sh | bash
#   bash install.sh
#
# Writes:
#   ~/.claude/skills/copy-studio/          and ~/.codex/skills/copy-studio/
#   brainstorming, writing-plans, copywriting, copy-editing, humanizer
#     in both skill folders, under those names
#   ~/.claude/commands/copy-studio.md
#
# The five dependencies are cloned from their upstream repositories and keep
# their own licenses. See scripts/install-deps.sh.
#
# Override the destinations with COPY_STUDIO_CLAUDE_HOME and
# COPY_STUDIO_CODEX_HOME (defaults: ~/.claude and ~/.codex).

set -euo pipefail

REPO_URL="https://github.com/Ekko237/copy-studio.git"

if [[ ! -f "${BASH_SOURCE[0]:-}" ]]; then
  if ! command -v git >/dev/null 2>&1; then
    echo "git is required." >&2
    exit 1
  fi
  tmp="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$tmp/copy-studio"
  set +e
  bash "$tmp/copy-studio/install.sh" "$@"
  status=$?
  set -e
  rm -rf "$tmp"
  exit "$status"
fi

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ ! -f "$ROOT/SKILL.md" || ! -f "$ROOT/scripts/install-deps.sh" || ! -f "$ROOT/commands/copy-studio.md" ]]; then
  echo "install.sh needs a copy-studio checkout (SKILL.md, scripts/install-deps.sh, commands/copy-studio.md)." >&2
  echo "From anywhere: curl -fsSL https://raw.githubusercontent.com/Ekko237/copy-studio/main/install.sh | bash" >&2
  exit 1
fi

# shellcheck source=scripts/install-deps.sh
source "$ROOT/scripts/install-deps.sh"

: "${COPY_STUDIO_CLAUDE_HOME:=$HOME/.claude}"
: "${COPY_STUDIO_CODEX_HOME:=$HOME/.codex}"
export COPY_STUDIO_CLAUDE_HOME COPY_STUDIO_CODEX_HOME

install_into "$ROOT" "${COPY_STUDIO_CLAUDE_HOME}/skills/copy-studio"
echo "Installed copy-studio -> ${COPY_STUDIO_CLAUDE_HOME}/skills/copy-studio"

install_into "$ROOT" "${COPY_STUDIO_CODEX_HOME}/skills/copy-studio"
echo "Installed copy-studio -> ${COPY_STUDIO_CODEX_HOME}/skills/copy-studio"

command_path="${COPY_STUDIO_CLAUDE_HOME}/commands/copy-studio.md"
mkdir -p "$(dirname "$command_path")"
if [[ -f "$command_path" ]] && ! cmp -s "$ROOT/commands/copy-studio.md" "$command_path"; then
  command_bak="${command_path}.bak-$(date +%Y%m%d-%H%M%S)-$$"
  cp "$command_path" "$command_bak"
  echo "Kept existing ${command_path} as ${command_bak}"
fi
cp "$ROOT/commands/copy-studio.md" "$command_path"
echo "Installed slash command -> ${command_path}"

install_dependencies

cat <<EOF

Done.
  Copy Studio:     ${COPY_STUDIO_CLAUDE_HOME}/skills/copy-studio
                   ${COPY_STUDIO_CODEX_HOME}/skills/copy-studio
  Slash command:   ${command_path}
  Dependencies:    brainstorming, writing-plans, copywriting, copy-editing, humanizer
                   in both skill folders, each with its upstream LICENSE.

Then fill in your own fact base (see references/channel-calibration-template.md)
and ask for /copy-studio, or describe the copy job.
EOF
