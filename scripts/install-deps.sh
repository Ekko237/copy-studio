#!/usr/bin/env bash
# Install the five skills Copy Studio calls, under the names it invokes.
#
#   bash scripts/install-deps.sh
#
# Clones each skill from its upstream repository into both skill folders:
#   ~/.claude/skills/<name>
#   ~/.codex/skills/<name>
#
# Those projects stay under their own licenses. This script copies each
# upstream LICENSE in next to the skill and does not relicense anything.
# Copy Studio is not part of this step; install.sh does that too.
#
# Override the destinations with COPY_STUDIO_CLAUDE_HOME and
# COPY_STUDIO_CODEX_HOME (defaults: ~/.claude and ~/.codex).

_copy_studio_cleanup() {
  if [[ -n "${COPY_STUDIO_WORKDIR:-}" ]]; then
    rm -rf "$COPY_STUDIO_WORKDIR"
    unset COPY_STUDIO_WORKDIR
  fi
}

install_into() {
  local src="$1" dest="$2"
  local src_phys dest_phys
  if [[ ! -d "$src" ]]; then
    echo "Missing source directory: $src" >&2
    return 1
  fi
  src_phys="$(cd "$src" && pwd -P)"
  dest_phys=""
  if [[ -d "$dest" ]]; then
    dest_phys="$(cd "$dest" && pwd -P)"
  fi
  # Running install.sh from a skill folder that is already the checkout.
  if [[ -n "$dest_phys" && "$src_phys" == "$dest_phys" ]]; then
    touch "$dest/.copy-studio-managed"
    return 0
  fi
  if [[ -e "$dest" && ! -f "$dest/.copy-studio-managed" ]]; then
    local bak
    bak="${dest}.bak-$(date +%Y%m%d-%H%M%S)-$$"
    mv "$dest" "$bak"
    echo "Kept existing ${dest} as ${bak}"
  elif [[ -d "$dest" ]]; then
    find "$dest" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
  fi
  mkdir -p "$dest"
  tar -C "$src" --exclude='.git' -cf - . | tar -C "$dest" -xf -
  touch "$dest/.copy-studio-managed"
}

skill_declared_name() {
  awk '
    /^---[[:space:]]*$/ { c++; next }
    c == 1 && /^name:[[:space:]]*/ {
      sub(/^name:[[:space:]]*/, "")
      gsub(/["'\'']/, "")
      sub(/[[:space:]]+$/, "")
      print
      exit
    }
  ' "$1"
}

clone_upstream() {
  local url="$1" dest="$2"
  shift 2
  local path missing
  rm -rf "$dest"
  if [[ "$#" -gt 0 ]]; then
    if git clone --depth 1 --filter=blob:none --sparse "$url" "$dest" &&
      git -C "$dest" sparse-checkout set "$@"; then
      if [[ ! -f "$dest/LICENSE" ]]; then
        git -C "$dest" checkout HEAD -- LICENSE >/dev/null 2>&1 || true
      fi
      missing=0
      for path in "$@"; do
        if [[ ! -d "$dest/$path" ]]; then
          missing=1
        fi
      done
      if [[ "$missing" -eq 0 ]]; then
        return 0
      fi
    fi
    echo "Sparse clone failed for ${url}; cloning the full default branch." >&2
    rm -rf "$dest"
  fi
  git clone --depth 1 "$url" "$dest"
}

write_upstream_note() {
  local dest="$1" url="$2" path="$3" sha="$4"
  cat >"$dest/UPSTREAM" <<EOF
${url}
${path}
${sha}
EOF
}

place_skill() {
  local name="$1" src="$2" repo_dir="$3" url="$4" path="$5"
  local declared license_note sha root dest stage
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Upstream ${name} has no SKILL.md at ${path:-.} in ${url}." >&2
    return 1
  fi
  declared="$(skill_declared_name "$src/SKILL.md")"
  if [[ "$declared" != "$name" ]]; then
    echo "Expected SKILL.md name '${name}' in ${url} (${path:-.}), found '${declared:-<none>}'." >&2
    return 1
  fi
  if [[ ! -f "$repo_dir/LICENSE" && ! -f "$src/LICENSE" ]]; then
    echo "Refusing to install ${name}: ${url} has no LICENSE file." >&2
    return 1
  fi

  sha="$(git -C "$repo_dir" rev-parse HEAD)"
  stage="${COPY_STUDIO_WORKDIR}/stage-${name}"
  rm -rf "$stage"
  mkdir -p "$stage"
  tar -C "$src" --exclude='.git' -cf - . | tar -C "$stage" -xf -
  if [[ ! -f "$stage/LICENSE" ]]; then
    cp "$repo_dir/LICENSE" "$stage/LICENSE"
    license_note="copied from the repository root"
  else
    license_note="shipped inside the skill folder"
  fi
  write_upstream_note "$stage" "$url" "${path:-.}" "$sha"

  for root in "$COPY_STUDIO_CLAUDE_SKILLS" "$COPY_STUDIO_CODEX_SKILLS"; do
    dest="${root}/${name}"
    install_into "$stage" "$dest"
    echo "Installed ${name} -> ${dest}"
  done
  echo "  ${name}: ${url} @ ${sha} (LICENSE ${license_note}; not relicensed)"
}

install_dependencies() {
  : "${COPY_STUDIO_CLAUDE_HOME:=$HOME/.claude}"
  : "${COPY_STUDIO_CODEX_HOME:=$HOME/.codex}"
  COPY_STUDIO_CLAUDE_SKILLS="${COPY_STUDIO_CLAUDE_HOME}/skills"
  COPY_STUDIO_CODEX_SKILLS="${COPY_STUDIO_CODEX_HOME}/skills"
  export GIT_TERMINAL_PROMPT=0

  if ! command -v git >/dev/null 2>&1; then
    echo "git is required to install the dependency skills." >&2
    return 1
  fi
  if ! command -v tar >/dev/null 2>&1; then
    echo "tar is required." >&2
    return 1
  fi

  mkdir -p "$COPY_STUDIO_CLAUDE_SKILLS" "$COPY_STUDIO_CODEX_SKILLS"

  local super market humanizer
  COPY_STUDIO_WORKDIR="$(mktemp -d)"
  trap _copy_studio_cleanup EXIT

  echo "Cloning dependency skills. Each stays under its own upstream license."

  super="${COPY_STUDIO_WORKDIR}/superpowers"
  clone_upstream "https://github.com/obra/superpowers.git" "$super" \
    skills/brainstorming skills/writing-plans
  place_skill brainstorming "${super}/skills/brainstorming" "$super" \
    "https://github.com/obra/superpowers.git" "skills/brainstorming"
  place_skill writing-plans "${super}/skills/writing-plans" "$super" \
    "https://github.com/obra/superpowers.git" "skills/writing-plans"

  market="${COPY_STUDIO_WORKDIR}/marketingskills"
  clone_upstream "https://github.com/coreyhaines31/marketingskills.git" "$market" \
    skills/copywriting skills/copy-editing
  place_skill copywriting "${market}/skills/copywriting" "$market" \
    "https://github.com/coreyhaines31/marketingskills.git" "skills/copywriting"
  place_skill copy-editing "${market}/skills/copy-editing" "$market" \
    "https://github.com/coreyhaines31/marketingskills.git" "skills/copy-editing"

  humanizer="${COPY_STUDIO_WORKDIR}/humanizer"
  clone_upstream "https://github.com/blader/humanizer.git" "$humanizer"
  place_skill humanizer "$humanizer" "$humanizer" \
    "https://github.com/blader/humanizer.git" ""
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  set -euo pipefail
  install_dependencies
fi
