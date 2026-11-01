#!/usr/bin/env bash
# add-to-repo.sh — pull gtd-board-kit into the current work repo as a pinned submodule.
#
#   bash add-to-repo.sh [<full-40-hex-commit>]
#
# Run from the work repo's root, on a branch (never the default branch). It adds the
# submodule at .gtd/kit pinned to the given commit (default: the kit's main), links the
# skills into .claude/skills and .codex/skills, adds a SessionStart hook if the repo has no
# .claude/settings.json, starts .gtd/BOARD.local.md (the repo's own layer) if missing, and
# points CLAUDE.md / AGENTS.md at both. It commits nothing:
# review `git status`, commit, and open a PR.
set -euo pipefail

KIT_URL="https://github.com/dandelion-love/gtd-board-kit"
KIT_DIR=".gtd/kit"
SKILLS=(board-onboard board-pickup board-claim board-report board-needs-person board-lane okf-knowledge)
PIN="${1:-}"

[ -d .git ] || { echo "run this from the work repo's root" >&2; exit 1; }
branch="$(git rev-parse --abbrev-ref HEAD)"
default="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's#^origin/##' || true)"
case "$branch" in main|master|"$default") echo "on $branch: switch to a branch first" >&2; exit 1 ;; esac

if [ ! -e "$KIT_DIR/.git" ]; then
  git submodule add "$KIT_URL" "$KIT_DIR"
fi
git -C "$KIT_DIR" fetch --quiet origin
[ -n "$PIN" ] || PIN="$(git -C "$KIT_DIR" rev-parse origin/main)"
[[ "$PIN" =~ ^[0-9a-f]{40}$ ]] || { echo "pin must be a full 40-hex commit" >&2; exit 1; }
git -C "$KIT_DIR" checkout --quiet --detach "$PIN"
git add .gitmodules "$KIT_DIR"

# Symlinks written straight into the index, so this works the same on every OS.
for tool in .claude .codex; do
  for s in "${SKILLS[@]}"; do
    path="$tool/skills/$s"
    if [ -e "$path" ] && [ ! -L "$path" ]; then
      echo "keep    $path (the repo's own skill overrides the kit's)"; continue
    fi
    target="../../$KIT_DIR/skills/$s"
    blob="$(printf '%s' "$target" | git hash-object -w --stdin)"
    git rm -r --cached --quiet --ignore-unmatch "$path"
    rm -rf "$path"
    git update-index --add --cacheinfo "120000,$blob,$path"
    git checkout -- "$path"
  done
done

if [ ! -e .claude/settings.json ]; then
  cp "$KIT_DIR/install/settings.snippet.json" .claude/settings.json
  git add .claude/settings.json
else
  echo "NOTE: .claude/settings.json exists; merge $KIT_DIR/install/settings.snippet.json into it by hand."
fi

if [ ! -e .gtd/BOARD.local.md ]; then
  cp "$KIT_DIR/install/BOARD.local.template.md" .gtd/BOARD.local.md
  git add .gtd/BOARD.local.md
  echo "NOTE: fill in .gtd/BOARD.local.md with this repo's labels, fields and rules."
fi

add_line() {  # file line
  if ! grep -qsF ".gtd/kit/BOARD.md" "$1"; then
    [ -s "$1" ] && printf '\n' >> "$1"
    printf '%s\n' "$2" >> "$1"
    git add "$1"
  fi
}
add_line CLAUDE.md "Board work (gtd-board-kit): @.gtd/kit/BOARD.md then @.gtd/BOARD.local.md"
add_line AGENTS.md "Board work (gtd-board-kit): read .gtd/kit/BOARD.md, then .gtd/BOARD.local.md, before touching the board."

echo "gtd-board-kit pinned at $PIN. Review, commit and open a PR:"
git status --short
