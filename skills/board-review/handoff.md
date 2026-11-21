# Reviewing a milestone handoff

Part of the `board-review` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md`
first. Use this when the thing to review arrives as a milestone handoff (a `handoff_list`
entry, or a signed packet comment on a server without the capability).

1. **Read it, then claim.** `handoff_get(repo, handoff_id)`. If `stale` is true or the
   handoff is not the `head`, stop and say so: ask the sender for the current one. Then
   `item_claim(purpose="review", session=..., handoff=handoff_id)`. The worker may still hold
   the item: naming the head handoff is what lets your review claim sit beside the worker's
   claim, and only the handoff's recipient may do it. Your claim, not the handoff, lets you
   work, and a session that did the work never reviews it.
2. **Acknowledge** with `handoff_ack(repo, handoff_id, delivery_id, revision)` once you have
   read the packet. A repeat is harmless. This says you received it, nothing more.
3. **Review the revision the handoff names**, not the branch tip.
4. **Write the verdict** with `issue_comment` carrying `review_stage`, `review_verdict`,
   `review_handoff` (the `handoff_id` you reviewed), `review_milestone` and `review_revision`
   (the handoff's own), so it names what it covers. A verdict is effective only from the
   handoff's recipient while your review claim is live. Findings go back as a handoff of your
   own: `action` `address-findings`, `recipient_role` `worker`, the same revision, on the
   milestone `<milestone>-findings` (its own head, so it never replaces the evidence head).
5. A verdict you cannot tie to a milestone and revision is not written. If the head moves
   while you review, your verdict is for the old revision and says so: it authorizes nothing
   newer.

On a server without the capability, do the same from the packet comment: name its milestone
and revision in your findings, and say delivery was manual.
