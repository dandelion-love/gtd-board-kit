---
name: board-needs-person
description: Ask a person for a decision, a spec, access or a ruling on a board item, mark it on the board with the right needs:* label, and stop work on it, through the gtd MCP server. Use whenever you would otherwise guess at something only a person can settle.
metadata:
  author: gtd-board-kit
  version: 0.3.0
---

# Ask a person, then stop

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's labels, columns and rules win over anything below.

## When

Use this instead of guessing when the answer needs a person: a product or design
decision, a missing acceptance spec, credentials or a click only they can make, a
deploy or merge, a review only a person can give, or an item you cannot classify. Do not use it for things you can find out yourself by reading the repo.

## Pick `needs`

`needs` names whom the item waits for; the server adds the label `needs:<needs>`. Use
only values this repo has: the profile's `needs:*` labels (`profile_get`) plus any in
`.gtd/BOARD.local.md`, which also says which one means "the owner". `triage` (new and
unsorted) exists everywhere. When unsure, use the owner's value.

## Ask

```
item_report(repo, number, attention="<the question>", needs="<needs>",
            state="waiting", note="<what you were doing>", links=[…], project)
```

- The server adds `needs:<needs>`; the bridge moves the card to the profile's
  needs-a-person column.
- Start `attention` with the @handle `.gtd/BOARD.local.md` maps to that `needs`
  ("Notifications"); with no map, mention nobody. That mention is the only ping: one
  per ask, again only if the question changes. Never mention for progress or thanks.
- Write one question a person can answer in a minute. Give the options and your
  recommendation, and what you will do with each answer. Link evidence, do not paste it.
- Omit `state` if you do not hold the item: anyone may ask, only the holder reports.
- If the item is not a GitHub issue you can report on, `issue_comment` the question and
  add the label with `issue_labels`.
- Never open a separate issue for the question: `question` is not a Kind. Open its own
  `chore` or `spike` only when answering it is real work, and link it as a blocker.

## Then stop

- Stop work on that item. In a standing lane, only that item stops; the lane goes on
  (`board-lane`). Release it with `item_release` if you will not be back before
  the lease ends (`next` = "answer the question above").
- Tell your person, in the session, what you asked and where.
- Do not remove the `needs:*` label yourself: taking it off is the person's call.
