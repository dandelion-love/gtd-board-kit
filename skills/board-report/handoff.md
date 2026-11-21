# Handing a milestone to another session

Part of the `board-report` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md`
first, and `.gtd/kit/knowledge/model/milestone-handoff.md`. Use this when you need an
independent review or answer on one milestone of an item you hold, not when you are done
with the item (that is `item_release`).

1. **Fix the evidence.** Push, and note the commit. A branch name is not evidence.
2. **Check the server.** `whoami` lists `capabilities`; the mode follows
   `server-spec/milestone-handoff.md` (Capability negotiation): `push`, `poll` or `manual`.
3. **Write the packet**: milestone, revision, evidence links, one ask from `review-plan`,
   `review-work`, `address-findings`, `answer-question`, `continue-work`, and what you do
   meanwhile. At most 1200 characters; links, not logs.
4. **Send it.** `push` or `poll`: `handoff_send(repo, number, milestone, revision, action,
   request, recipient_role, evidence)`. For a newer revision of the same milestone, pass
   `supersedes` with the head's `handoff_id` (read it with `handoff_get`). `manual`: post the
   packet with `issue_comment`, link it in an `item_report`, and tell your person delivery
   is manual.
5. **Keep working.** Do the independent work you are claimed for; do not hold your lease idle
   or poll in a loop. Report `waiting` on this milestone only if nothing else is left.
6. **Read the answer** at your next `activity_since`, or with `handoff_get`. Act on a verdict
   only if it names this milestone and the head's revision (`effective` true) and comes from your recipient. Findings you sent go on `<milestone>-findings`. A stale verdict
   means send a new handoff, not argue with it.

Never say a release, a report or a comment wakes the recipient. Delivered is not
acknowledged, and acknowledged is not done. Never write the handoff's marker by hand.
