# Workflow templates

Agents never create or edit `.github/workflows/**` (BOARD.md rule 9), so the kit ships
workflows as templates here and a person installs them.

## gtd-pr-check.yml

Runs [`tools/pr_check.py`](../../tools/pr_check.py) on every pull request, and once a day
in `--audit` mode.

On a pull request it reports, for each issue the PR carries (`Closes`, `Fixes`,
`Resolves`, `Works on` or `Refs`, plus the issues in the `gtd-pr` marker):

- an `## Evidence` table row, with a result, for every `AC<n>` in the issue's
  `## Acceptance criteria` (with several issues, the row names its issue: `#<n> AC1`);
- a `## Test changes` section that names every test file the diff changes;
- the `gtd-pr` marker that `pr_open` writes (a PR without one was opened another way);
- a claim record on the issue, by the principal the marker names.

The daily audit reports, for the last 24 hours: `agent-ready` added by an agent or a
bot, merges and approvals by an agent or a bot, and pull requests opened without the
`gtd-pr` marker. A label the gtd server added is flagged with a note, because GitHub
records only the server as the actor; the claim and report records say who asked.

### Install (a person, once per repo)

1. Repin the kit so `.gtd/kit/tools/pr_check.py` exists.
2. Copy `.gtd/kit/templates/workflows/gtd-pr-check.yml` to
   `.github/workflows/gtd-pr-check.yml` and commit it yourself.
3. Optional: set the repository variables `GTD_SERVER_LOGIN`, `GTD_AGENT_LOGINS` and
   `GTD_RECORD_AUTHORS` (see the comments at the top of the template).

It needs read access only (`contents`, `issues`, `pull-requests`) and checks out the
base commit, so the PR under check never runs its own code.

### Report-only, then required

It starts report-only: findings appear in the job summary and the job stays green. Once
the reports look right, add `--enforce` to the pr-check step (exit 1 on any finding) and
mark the job a required status check in the branch rules. A required check needs a plan
that offers branch rules on the repo; without one, keep it report-only and read the
daily audit.

### Run it locally

```bash
GITHUB_TOKEN=... python3 .gtd/kit/tools/pr_check.py --repo owner/repo --pr <n>
GITHUB_TOKEN=... python3 .gtd/kit/tools/pr_check.py --audit --repo owner/repo --since 7d
```

The token is read from the environment and never printed. Exit status: 0 (report-only,
or no findings), 1 (findings with `--enforce`), 2 (usage or API error).
