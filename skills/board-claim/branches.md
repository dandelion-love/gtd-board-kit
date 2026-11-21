# Several stories on one branch

Part of the `board-claim` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md` first.

Your unit of work may be one or more stories, and the session that owns them may combine
them on one integration (release-candidate) branch.

- **Claim every story you work on**, one `item_claim` each, before its first commit.
  An unclaimed story never gets a commit, even on a combined branch. Refused on one?
  Leave it out of the batch.
- Each claim has its own lease, reports and release. Dropping a story: take its commits
  off the branch and release it.
- The PR lists every story it carries in `pr_open`'s `issues`. Before opening it, check
  each: you hold it (`item_get`), or it reached the combined branch through its own
  merged PR (the evidence for a released item).
