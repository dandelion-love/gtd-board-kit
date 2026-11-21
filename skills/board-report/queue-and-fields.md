# Queue order and ETA

Part of the `board-report` skill. Read `.gtd/kit/BOARD.md` and the skill's `SKILL.md` first.

Both are native board constructs, so a person changes them in the GitHub UI or API and
you follow on your next read. `.gtd/BOARD.local.md` names the view and fields; the
defaults are below.

- **Queue:** the card order in the queue view (a view with no sort, since a sort hides
  manual order). `project_items` returns items in board order; take the first one you
  may claim. Move a card only to put work you capture or hand back where the repo says,
  with `project_item_move`; never reorder what a person ordered.
- **ETA:** the `Target date` field (start: `Start date`), set with
  `project_set_field(field="Target date", value="YYYY-MM-DD")`. Put the same date in
  the `item_report` note. Before changing it, read it with `project_item_find`: if it
  differs from the date you last reported, a person set it. Keep theirs, and if you
  can't make it, say so in a report instead of moving it.
- **Order between items:** native blocked-by links (`issue_blocked_by_list`), never a
  note in the body.
- **Other fields:** `.gtd/kit/knowledge/model/board-fields.md` says who writes each
  field and when. Waiting on a person's gate: `Gates` names it and the report note is
  the one-line ask; once it passes, update `Gates` and clear the `needs:*` label.
- **Sync-owned fields:** a field a profile sync `owns` (`profile_get`; in ml-lab an
  experiment's Agent, Start date and Last report) is written by the sync from its
  register. Never set it by hand, not even for an ETA or a note: record the event
  (`experiment_record`) and let the sync write the card. A Status stuck after a run
  ended means its register event or PR never landed: land it, never move the card.
