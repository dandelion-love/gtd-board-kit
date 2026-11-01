# This repo's board layer

Read after `.gtd/kit/BOARD.md`. Where this file differs from the kit, this file wins,
except that it can never relax the kit's rule 1 (board only through the gtd MCP server)
or rule 9 (hard limits). It lives in this repo, not in the public kit, so it is the place
for anything specific to this repo. Delete any section you don't need.

## Board and profile

- Profile: <!-- as in .github/gtd-context.json -->
- Board: <!-- owner/number -->
- Other boards or channels agents here may write to: <!-- e.g. a run-state channel -->
- The owner's `needs` value: <!-- the needs:* label that means "only the owner can unblock this" -->

## Labels this repo adds or uses differently

| Label | Meaning here | What an agent does with it |
| --- | --- | --- |
| | | |

## Status per label (only if this repo has no label-to-Status bridge)

| Label | Status column |
| --- | --- |
| agent-running | |
| waiting-for-review | |
| blocked | |

## Fields and columns

<!-- Fields beyond the profile and who writes them; columns an agent must never set by hand. -->

## What agents may pick up here

<!-- Tighten or loosen the kit's pickup rule, e.g. which item types an agent may pull. -->

## Procedure differences

<!-- Steps that replace or add to the kit skills. For a bigger change, put a repo-owned
     skill in .claude/skills/<name>/ (a real folder, not a link); one with a kit skill's
     name replaces it. -->
