---
name: board-onboard
description: Connect this repo to its board, or check and repair that connection. Covers the kit install, gtd MCP access, drafting .gtd/BOARD.local.md from the repo and the board, and the PR. Use when asked to onboard, set up, connect or check a repo's board, when .gtd/BOARD.local.md is missing or unfilled, or after moving the kit pin.
metadata:
  author: gtd-board-kit
  version: 0.1.0
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

## Never

- Put anything about this repo into the kit, which is public. It all goes in
  `.gtd/BOARD.local.md`.
- Merge your own PR, commit to the default branch, or edit `.github/workflows/**`.
- Print or ask for a credential.
