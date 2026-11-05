---
name: board-needs-person
description: Ask a person for a decision, a spec, access or a ruling on a board item, mark it on the board with the right needs:* label, and stop work on it, through the gtd MCP server. Use whenever you would otherwise guess at something only a person can settle.
metadata:
  author: gtd-board-kit
  version: 0.5.0
---

# Ask a person, then stop

Read `.gtd/kit/BOARD.md`, then `.gtd/BOARD.local.md` if it exists, first if you have not
this session; the local file's labels, columns and rules win over anything below.

## When

Ask only for a **stop reason** (`.gtd/kit/knowledge/decomposition/human-gates/attention-budget.md`):
spending, deleting or anything irreversible; grants, policy or lane switches; research or
product direction; work outside the item's scope. A missing acceptance spec, credentials
or a click only a person can make also stop the item. Never guess at these.

Anything else inside a mandate you already have is yours to decide: pick, record the
choice and how to undo it on the item, keep going. Do not re-ask for a go-ahead you were
given. A question that does not block the work waits for the hand-back: it is the one
action in your `ready` report (`board-report`), not a `waiting` stop. Do not use this
for things you can find out yourself by reading the repo.

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
- **Who gets pinged.** If the server lists `notify_get`, it pings for you: write no
  @mention in `attention`. Check the result's `ping`: `posted` or `unchanged` is fine;
  `no-map` or `no-identity` means nobody was pinged, so tell your person the ask is on
  the board but unpinged. One ping per ask; asking the same question again pings nobody.
- Without `notify_get`, start `attention` with the @handle `.github/gtd-context.json`
  maps to that `needs` under `notify.mentions` (or `.gtd/BOARD.local.md`,
  "Notifications"); with no map, mention nobody. Mention once per ask, again only if the
  question changes, never for progress or thanks. A mention written under the mentioned
  person's own account notifies nobody: if records are written as that person, leave it
  out and tell your person the ask is unpinged.
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
