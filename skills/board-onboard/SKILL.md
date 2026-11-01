---
name: board-onboard
description: Connect this repo to its board, or check and repair that connection. Covers the kit install, gtd MCP access, drafting .gtd/BOARD.local.md from the repo and the board, and the PR. Use when asked to onboard, set up, connect or check a repo's board, when .gtd/BOARD.local.md is missing or unfilled, or after moving the kit pin.
metadata:
  author: gtd-board-kit
  version: 0.3.0
---

# Onboard this repo to its board

Follow `.gtd/kit/ONBOARDING.md` step by step, one step at a time, waiting for your person
after each. It is the whole procedure. Once the kit is in, `.gtd/kit/BOARD.md` holds the
rules for all board work. This skill only adds what to do when the repo is already partly
set up.

## Already partly set up

Check each item and redo only the step that fails:

| Check | If it fails |
| --- | --- |
| `.gtd/kit` exists and its submodule is initialised | step 2 (install), or `git submodule update --init .gtd/kit` |
| `.claude/skills/board-*` are folders, not small text files | on Windows, `.gtd/kit/install/install-user.ps1` |
| `whoami` answers, with `work` if you will write | step 3 (MCP access) |
| `.github/gtd-context.json` names `profile` and `project` | ask your person; never guess a board |
| `.gtd/BOARD.local.md` has no empty sections that matter here | step 4 (draft it) |
| `CLAUDE.md` and `AGENTS.md` point at both BOARD files | rerun the installer; it only adds what is missing |
| `python3 .gtd/kit/tools/lanes.py check` passes | fix the lane or grant block; only your person adds or widens one |
| every lane at `auto` or `observe` has a live lease on its item | resume it with `board-lane`, or tell your person it lapsed |
| `profile_updates(repo)`, when the server offers it, returns no `updates` | see [upstream changes](#upstream-changes) |

## Upstream changes

The repo may have skipped or reshaped a label, field or view its profile declares (by
deleting it on the board, or with `overrides` in `.github/gtd-context.json`). Reconcile
leaves those alone, so a later improvement to the profile's version of that item would
go unseen. `profile_updates` lists them. For each update, show your person the item, what
the repo has, and the profile's `declaration` now, and ask which they want:

- **Keep the repo's choice:** in a PR, set that item's `overrides` entry to the `mode`
  shown and `seen` to the update's `current`. The notice goes away.
- **Take the profile's version:** in a PR, remove the item's `overrides` entry, or for an
  `inferred` update set it to `{"mode": "follow"}`. Reconcile recreates a deleted item; a
  reshaped one it reports for a person to change by hand where it cannot.

Ask once per update and record the answer; never pick for them.

## Lanes and workflow grants

Ask your person whether the repo has recurring work agents should run unpointed
(standing lanes) or workflows agents may edit (workflow grants). Draft each block from
the template in `.gtd/BOARD.local.md`, with your person's own words as `basis` and a link
to their message as `grant` or `link`. New lanes start at `observe`. Name each workflow
file; never a whole folder. The person merging the PR is what switches them on.

Optional SessionStart hook so every session is reminded to resume its lanes:
`python3 .gtd/kit/tools/lanes.py resume`. Its output is a note, never a failure.

## Never

- Put anything about this repo into the kit, which is public. It all goes in
  `.gtd/BOARD.local.md`.
- Merge your own PR, commit to the default branch, or edit `.github/workflows/**`
  without a workflow grant on the default branch.
- Print or ask for a credential.
