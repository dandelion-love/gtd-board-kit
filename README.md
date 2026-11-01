# gtd-board-kit

Skills and rules that let any agent (Claude Code or Codex, cloud or desktop) work a
dandelion-love board **through the hosted gtd MCP server**: find work, claim it, report
progress, ask a person, hand back a PR. Every work repo pulls this repo in as a pinned
git submodule at `.gtd/kit`.

This repo is public on purpose: a cloud session can fetch its own repo and public repos,
but not a second private one. It holds only Markdown and install scripts, never runtime
data, tokens or board contents.

| Path | What |
| --- | --- |
| `BOARD.md` | The rules every agent reads first (under 3 KB) |
| `ONBOARDING.md`, `skills/board-onboard` | Connect a repo to its board, step by step; any agent can read it from the public URL |
| `skills/board-pickup` | Find an item this agent may take (read-only) |
| `skills/board-claim` | Claim it, work it on `gtd/issue-<n>`, hand back a PR |
| `skills/board-report` | Report progress, renew, release, record failure |
| `skills/board-needs-person` | Ask a person with the right `needs:*` label, then stop |
| `skills/board-lane`, `tools/lanes.py` | Standing lanes: recurring pre-approved work with its own switch; run a tick, resume schedules, lint lanes and workflow grants |
| `okf/`, `skills/okf-knowledge`, `tools/okf_lint.py` | The pinned Open Knowledge Format spec, the authoring skill, and its linter |
| `knowledge/` | The kit's own design notes, as an OKF bundle |
| `server-spec/` | For builders: what a gtd MCP server must do so this kit works against it, cut into buildable units with conformance checks |
| `conformance/` | A ready-to-run, black-box runner for those checks: point it at any server URL and get pass or fail per check |
| `install/` | `add-to-repo.ps1` / `.sh`, `install-user.ps1`, the SessionStart hook, the `BOARD.local.md` starter |
| `tests/check_kit.py` | Size budgets, frontmatter, versions, links, and the public guard over the tree |
| `tools/public_guard.py`, `.githooks/` | The guard that keeps private data out: `pre-commit`, `commit-msg`, `pre-push` |
| `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json` | Rules for any agent working on the kit, and Claude Code hooks that run the guard |

## Knowledge docs: OKF, pinned by the kit

Repos that use the kit keep their knowledge docs (findings, decisions, references) as an
[Open Knowledge Format](okf/README.md) bundle at the version in `okf/PIN.json`, currently
OKF 0.2. The spec travels with the kit, so moving a repo's kit pin is how it moves to a
newer OKF. Lint a bundle with:

```bash
python3 .gtd/kit/tools/okf_lint.py docs/knowledge --strict
```

## Onboard a repo (the one-line handoff)

Point any agent at a work repo with:

> Read https://raw.githubusercontent.com/dandelion-love/gtd-board-kit/main/ONBOARDING.md
> and follow it for this repo.

It installs the kit, gets MCP access, drafts the repo's `.gtd/BOARD.local.md` from the
repo and the board, and opens a PR, one step at a time with its person. Nothing about the
repo leaves the repo.

## Add it to a work repo by hand

On a branch in the work repo's root:

```powershell
# Windows PowerShell
git switch -c gtd/board-kit
iwr https://raw.githubusercontent.com/dandelion-love/gtd-board-kit/main/install/add-to-repo.ps1 -OutFile $env:TEMP\add-to-repo.ps1
powershell -ExecutionPolicy Bypass -File $env:TEMP\add-to-repo.ps1
```

```bash
# bash (Linux, macOS, WSL, cloud)
git switch -c gtd/board-kit
curl -fsSL https://raw.githubusercontent.com/dandelion-love/gtd-board-kit/main/install/add-to-repo.sh | bash
```

It adds the submodule pinned to a full commit, links the kit's skills into
`.claude/skills` and `.codex/skills`, adds a SessionStart hook that initialises the
submodule in fresh cloud clones, and adds one line to `CLAUDE.md` and `AGENTS.md`. It
commits nothing. Review, commit, open a PR, and let a person merge it.

The repo also needs `.github/gtd-context.json` with its `profile` and `project`, and the
agent needs the gtd MCP server: claude.ai cloud threads use the connector; everything
else joins at `<server>/join`.

## Build a compatible server

The kit talks to "the gtd MCP server" through a fixed set of tools, a join flow and a
record format on issues. [`server-spec/`](server-spec/README.md) specifies all of it
without naming any deployment: transport and identity, the agent join, profiles and
labels, claim records and their fold, every tool's contract, security rules, numbered
conformance checks, and a work plan a coding agent can build one unit at a time.
[`conformance/`](conformance/README.md) runs those checks against any server over HTTP,
whatever it is written in.

## Customise per repo

Each repo layers its own rules on top of the kit without touching it:

- `.gtd/BOARD.local.md` (started from `install/BOARD.local.template.md`): extra labels,
  fields, columns, boards, pickup limits, procedure, and the Status column per label for
  repos without the label bridge. Keep everything repo-specific there, in the private
  repo: this kit is public. Agents read it right after
  `BOARD.md`, and it wins where they differ, except rule 1 (MCP only) and rule 9 (hard
  limits).
- **Standing lanes** in `.gtd/BOARD.local.md`: recurring work a person approved once,
  each with `asked_by`, `basis`, a `grant` link, a `policy` version, a switch
  (`auto`, `observe`, `hold`, `off`), its own board item whose lease is the heartbeat,
  and `may` / `never` lists. Scheduled prompts only point at the lane; the
  `board-lane` skill re-creates schedules after a restart.
- **Workflow grants** in `.gtd/BOARD.local.md`: the one way rule 9 opens. Each grant
  names the workflow files, who granted it, when, and a link. Agents still branch, open
  a PR and never merge. No grant: never.
- A real folder at `.claude/skills/<name>` (and `.codex/skills/<name>`) is the repo's own
  skill. One named like a kit skill replaces it; the installer leaves it alone.
- The label-to-Status bridge already takes a local map at
  `.github/gtd-label-status-map.json`.

## Upgrade

Move the pin by PR in the work repo: `git -C .gtd/kit fetch; git -C .gtd/kit checkout
<sha>; git add .gtd/kit`. Never edit files inside `.gtd/kit`.

## Change the kit

Read [AGENTS.md](AGENTS.md) first: this repo is public, so nothing private may enter it.
Then: `git config core.hooksPath .githooks` once per clone, branch, edit, run
`python3 tests/check_kit.py`, bump `VERSION` and each changed skill's `metadata.version`,
and open a PR. The hooks run `tools/public_guard.py` on every commit and push; Claude Code
also runs it before any git commit, push or GitHub write. Private terms the built-in rules
can't know go in a denylist outside the repo (`~/.config/gtd/public-denylist.txt`).
