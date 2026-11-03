# Issue templates

The epic and story bodies `board-decompose` writes, as GitHub Markdown issue templates.
A person copies them into a work repo's `.github/ISSUE_TEMPLATE/` so issues opened in
the web UI start with the same sections an agent fills. The source of truth is
[`skills/board-decompose/templates.md`](../../skills/board-decompose/templates.md);
change both together.

- `epic.md`: Problem, Outcome check, Scope, Out of scope, Stories, Decisions, Risks and
  open questions, Gates. The Issue Type is preset to `Epic`.
- `story.md`: what changes and why, numbered acceptance criteria with evidence, steps.
  The Issue Type is preset to `Story`.

Templates are a UI aid: an issue created through the API (as agents do) gets no
template, which is why the skill writes the same body itself. A repo without
organization Issue Types deletes the `type:` line.
