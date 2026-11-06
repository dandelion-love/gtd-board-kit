# Onboarding: connect a repo to its board

For any agent (Claude, Codex, Muse, other) asked to connect a work repo to its board, or
to check that connection. Your person can hand you the whole job in one line:

> Read https://raw.githubusercontent.com/dandelion-love/gtd-board-kit/main/ONBOARDING.md
> and follow it for this repo.

Once the kit is installed, the same steps are the `board-onboard` skill, and this file is
at `.gtd/kit/ONBOARDING.md`.

## Ground rules

- Do one step at a time. Show your person the result and wait before the next step.
- Use the shell you are in. On Windows that is PowerShell with Windows paths. Check that a
  tool exists before you use it.
- Never print, paste or log a credential, and never ask your person to paste one.
- Every detail about this repo (board, labels, people, channels, hosts) goes into this repo's
  `.gtd/BOARD.local.md`. **Nothing goes upstream into the kit**: it is a public repo.
- Work on a branch. Commit nothing to the default branch, and never merge your own PR
  unless a merge grant in `.gtd/BOARD.local.md` covers every file in it.

## 1. Look at the repo

Show your person: the repo root, `git status`, the current branch, the origin remote, and
`.github/gtd-context.json`. That file should name the `profile`, the board as
`project`, and the MCP server as `mcp_url`. If it is missing or looks wrong, stop and ask.
Do not invent a board or a server address.

## 2. Add the kit (skip if `.gtd/kit` exists)

Switch to a branch, `gtd/board-kit`, then run the installer from the kit:

```powershell
iwr https://raw.githubusercontent.com/dandelion-love/gtd-board-kit/main/install/add-to-repo.ps1 -OutFile $env:TEMP\add-to-repo.ps1
powershell -ExecutionPolicy Bypass -File $env:TEMP\add-to-repo.ps1
```

```bash
curl -fsSL https://raw.githubusercontent.com/dandelion-love/gtd-board-kit/main/install/add-to-repo.sh | bash
```

It adds the pinned submodule, links the skills, adds a SessionStart hook, starts
`.gtd/BOARD.local.md`, and adds one line each to `CLAUDE.md` and `AGENTS.md`. Show your
person its output, including any NOTE lines.

On Windows, if `.claude\skills\board-pickup` turns out to be a small text file rather than
a folder, run `.gtd\kit\install\install-user.ps1` so the skills load.

## 3. Reach the gtd MCP server

Call `whoami`.

- It works: note the principal and the preset. Writing needs the `work` preset.
- The tools are missing in a claude.ai cloud thread: ask your person to connect the gtd
  connector in their claude.ai settings, with the address `<mcp_url>/mcp?agent=<name>`
  and "Sign in as an agent" on the approval page, then continue. If the connector exists
  but its sign-in expired, they reconnect it. Do not try the join client from the cloud
  container: its network policy may block the server, and it cannot keep the credential.
- `whoami` shows your person's own principal (for example `google:<email>`) instead of
  `agent:<name>`: the connector signed in as them, so your work is recorded under their
  name. Ask them to reconnect as an agent if this repo wants agent names.
- The tools are missing anywhere else: follow `<mcp_url>/join`, with `mcp_url` from
  `.github/gtd-context.json` (if it is missing, ask your person for the address and add it
  to that file in this PR). You run the join client; your person opens the link and
  approves. Ask for the smallest preset that does the job. The rules for keeping and renewing that access
  are in [agent sign-in](knowledge/model/agent-sign-in.md).

## 4. Draft `.gtd/BOARD.local.md`

Fill it from what the repo and the board say, not from memory:

- `profile_get` for the profile: its columns, labels, `needs:*` values and fields.
- `project_get` and `project_views_list` for the board in `.github/gtd-context.json`.
- Does `.github/workflows/project-sync.yml` exist? If not, fill the Status-per-label table.
- `project_workflows` on the board: with no sync that owns Status on close, ask your person
  to turn on **Item closed** and **Pull request merged**, both setting `Done`, on the board's
  Workflows page (no API can); with one, both stay off
  ([closed is Done](knowledge/model/board-fields.md#closed-is-done)).
  Take it from the profile when `profile_get` shows the map; otherwise ask your person.
- The repo's own README, `CLAUDE.md` and `AGENTS.md`: domain rules, channels, hosts, and
  steps agents must follow.
- Ask your person for what only they know: which `needs` value means the owner, what agents
  may pick up without being pointed at it, and anything that must never be touched.
- Ask who each `needs` value should ping, and whether new issues should reach the
  owner beyond the Inbox view (default: they wait in the view). Put the answer in
  `.github/gtd-context.json` under `notify` and note it in "Notifications".

- Ask whether agents here should run recurring work unpointed (standing lanes) or may
  edit named workflows (workflow grants). Draft those blocks with the person's own words
  and a link to them; new lanes start at `observe`. `python3 .gtd/kit/tools/lanes.py
  check` lints them.

Show the draft and change it until your person agrees.

Recommend OKF for the repo's knowledge docs: add the "Knowledge bundle" line (default
`docs/knowledge/`). If the repo already keeps OKF docs at an older version, offer to
migrate them with the `okf-knowledge` skill in a separate PR.

## 5. Open the PR

Commit on the branch, push, and open a PR that lists what the installer added and what
`BOARD.local.md` says. Your person reviews and merges it. Then restart the session so the
skills load.

## 6. Check it works

Read `.gtd/kit/BOARD.md` and `.gtd/BOARD.local.md`, then run `board-pickup` (it only
reads). Report what it found, or why nothing qualified.

## Re-running

Every step is safe to repeat. To upgrade the kit, move the pin in a PR:
`git -C .gtd/kit fetch`, `git -C .gtd/kit checkout <full-commit>`, `git add .gtd/kit`.
Then read the kit's README for anything new to add to `BOARD.local.md`, and lint the
knowledge bundle against the newly pinned OKF.
