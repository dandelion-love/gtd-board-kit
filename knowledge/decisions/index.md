# Decisions

* [The kit is a public, pinned submodule](kit-is-a-public-pinned-submodule.md) - How every repo gets the same board skills
* [The kit is the interface; each repo is an implementation](kit-is-the-interface.md) - General meaning in the kit, concrete meaning in the repo, native constructs as state
* [Each repo customises in its own layer](per-repo-layer.md) - Repo specifics live in the repo, never in the kit
* [Standing lanes are written rules a person switches on](standing-lanes.md) - Recurring pre-approved work, its switch and its heartbeat
* [A repo may grant workflow edits by name](workflow-grants.md) - The one way the workflow ban opens
* [OKF is pinned by the kit](okf-pinned-by-the-kit.md) - Knowledge docs follow one OKF version, moved with the kit
* [Work items live on the board; a local file is only a cache](work-items-live-on-the-board.md) - The issue is the record, a markdown copy is never committed
* [How work decomposes into epics, stories and steps](decomposition-standard.md) - Levels, Kinds, ready and done, the unit of agent work, PR authorship and gates
* [Agents pull new activity with one read](agents-pull-new-activity.md) - activity_since over held items, PRs opened for the agent and channels, with a read_at cursor
* [Requests between projects go through an intake and get an ack](intake-and-acks.md) - intake_list and intake_ack, observe-first intake lanes, and a needs flag when no ack comes
* [Notify a person only when they must act](notify-only-when-a-person-must-act.md) - Three reasons to push, through GitHub's mention or review request; new issues wait in views; an optional Web Push channel copies asks, with actions that only open or defer
* [Titles and summaries say what an item delivers](clear-titles-and-summaries.md) - Verb-first outcome titles with no prefix, subtitle, list or code; bodies open with who it helps and what changes; mechanical failures make a story not ready
