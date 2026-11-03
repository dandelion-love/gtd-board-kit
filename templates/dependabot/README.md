# Kit repins by Dependabot

`dependabot.yml` makes GitHub's own Dependabot open a pull request in a work repo
whenever the kit's `main` moves. No workflow file, token or secret is needed, so an
agent may add it (it is not under `.github/workflows/`).

1. Copy `dependabot.yml` to `.github/dependabot.yml` in the work repo, by PR. If the
   repo already has one, add the `gitsubmodule` entry to its `updates` list.
2. Create the `kit-repin` label, or delete the `labels` lines.
3. A private kit fork needs Dependabot access to it (organization settings); the
   public kit needs nothing.

Each PR moves `.gtd/kit` by one release. Before merging, read that release's line in
the kit's `knowledge/log.md`: when it adds a repo step (such as copying
`templates/issues/` or a new `BOARD.local.md` row), do it on the same branch.
