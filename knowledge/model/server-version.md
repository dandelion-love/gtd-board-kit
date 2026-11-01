---
type: Pattern
title: Server version and levels
description: The server says which spec version it implements and which conformance levels it meets; an agent compares the version with its kit pin, runs only the skills whose level is claimed, and tells its person once about a mismatch.
tags: [mcp, conformance, versioning]
status: draft
generated: { by: claude-code/cloud, at: 2026-11-01T18:45:00Z }
---

# Rule

The server declares two things, in `whoami` and, without signing in, at
`<mcp_url>/.well-known/gtd-board-kit` (the server side is "Spec version and levels" in
`server-spec/transport-and-identity.md` in this kit):

- `spec_version`: the kit version whose server spec it implements;
- `conformance`: the levels it meets right now (`Core`, `Join`, `Board`, `Extended`),
  claimed only when their checks pass.

The repo's own kit version is `.gtd/kit/VERSION`. Read both at the start of a session,
with `whoami` (BOARD.md rule 1).

# Levels decide what runs

Each kit skill needs a level (the levels table in `server-spec/README.md`):
`board-pickup`, `board-claim`, `board-report`, `board-needs-person` and `board-lane` need
`Core`; a repo with no label bridge also needs `Board`; a procedure in
`.gtd/BOARD.local.md` that names an optional tool needs `Extended` and that tool in
`tools/list`.

- **Level claimed:** run the skill.
- **Level missing:** do not run it, and do not work around it with a token, GraphQL or
  `gh` (rule 1). Tell your person which level is missing and what it blocks, then do
  work that does not need it.
- **Empty list:** no board work here. Say so and stop board work for the session.

# The version is a signal

Compare `MAJOR.MINOR` of `spec_version` with the kit's (before 1.0 any minor bump may
change the contract; after 1.0, only a major one).

| Server vs kit | What it means | What to do |
| --- | --- | --- |
| Same | The skills and the server agree | Work normally |
| Server newer | The repo's kit pin is behind | Work within the claimed levels; tell your person the pin could move up. Move it only when asked |
| Server older | The kit may call tools or fields the server lacks | Work within the claimed levels; check `tools/list` before a tool the server may not have; a missing field is unknown, not empty. Tell your person the server is behind |
| No `spec_version` | A server from before this rule | Treat the levels as unknown: run a skill only when every tool it calls is in `tools/list`, and tell your person |

Say a mismatch **once per session**, in one line with both versions, in your reply to
your person. It is not an item report and not a `needs:*` label: it is about the
deployment, not about an item.

# Why

Agents and servers move on different clocks: a work repo pins the kit, while a server is
redeployed on its own schedule. Without a declared version and honest levels an agent
cannot tell "this tool is missing" from "I am on the wrong server", and guesses. See
[the kit is the interface](/decisions/kit-is-the-interface.md).
