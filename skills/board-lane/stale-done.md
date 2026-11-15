# Sweeping for finished items

A lane whose `may` list says so, and a repo without `sweep: off` in its `## Stale done`
block of `.gtd/BOARD.local.md`, runs one sweep per tick: `stale_done(repo,
branches=<landed_branches, if set>)`, then `item_close_done` for each entry with verdict
`close`. A lane never closes by `issue_close`, and never closes an item `stale_done` keeps.
Report the tick once: each item closed, with its link (a person's undo is `issue_reopen`),
and each `keep` that has merged work and only `unmet-criteria` as its reason. A tick with
neither reports nothing. Under `observe`, write `would close: <items>` instead.

