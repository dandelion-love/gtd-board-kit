# 11. Typed links between items

Work items and register records point at each other: one experiment was designed from
another's result, a listening test judges two experiments, a finding rests on a result, a
newer benchmark replaces an older one. This section fixes how such a link is written, how a
server folds the links of a repo's records into edges, and how a sync shows them on the
mirrored issues. The model behind it, and why most kinds are text, is in
[typed links](../knowledge/model/typed-links.md).

It applies to a server that offers `work_items_sync` (the Repo setup group in
[tools](tools.md#optional-groups)) for a profile whose sources produce items from register
files. A server that writes register lines for a caller (a tool that appends a `link` line)
also follows [writing a link](#writing-a-link).

## The link record

A link is one line in an append-only register, written by whoever records it:

```json
{"event": "link", "from": "EXP-2", "to": "EXP-1", "kind": "follows-up",
 "why": "designed from EXP-1's verdict", "by": "agent:name", "t": "2026-11-04 15:00:00+00:00"}
```

- `from` and `to` name items by id. A register in which every line carries `id` MAY write
  `id` in place of `from`; a reader takes `from` when present, else `id`.
- `to` makes it an **item link**. A `link` line with a `url` and no `to` is an artifact
  pointer (a page, a PR, a checkpoint), not an edge, and the fold ignores it. A version 1
  record writes a pointer as an `artifact` event instead ([register records](register-records.md)),
  and a reader upgrades such a `link` to one.
- `kind` is one of the kinds below. A free-text kind is refused: a graph whose edge names
  drift cannot be walked.
- `why` says what the link asserts, in a sentence. A writer requires it; a reader accepts
  older lines without it.
- A register MAY derive links from a registration's own fields instead of separate lines
  (a listening test's list of the experiments it judges is `evaluates`; a finding's list of
  the results it rests on is `rests-on`). A profile source names such fields; they fold as
  link records at the registration's place in the register.
- `{"event": "unlink", "from", "to", "kind", "why"}` takes a link back. The register stays
  append-only; the edge goes.

## Kinds

| Kind | Read from the far end | `from` ... `to` | On GitHub |
| --- | --- | --- | --- |
| `depends-on` | `blocks` | `from` cannot start or end until `to` has | a **native blocked-by** link (`from` blocked by `to`), and a Related line |
| `follows-up` | `followed-up-by` | `from` was designed from `to`'s result | Related line |
| `references` | `referenced-by` | `from` uses `to` as its comparison arm or baseline | Related line |
| `evaluates` | `evaluated-by` | `from` (a test, a benchmark) judges `to`'s output | Related line |
| `rests-on` | `supports` | `from` (a finding) rests on `to`'s result | Related line |
| `refines` | `refined-by` | `from` narrows or qualifies `to`'s reading | Related line |
| `contradicts` | `contradicts` | the two cannot both be right; `why` says which | Related line |
| `corroborates` | `corroborates` | independent evidence pointing the same way | Related line |
| `supersedes` | `superseded-by` | `from` replaces `to` as the one to use | Related line |
| `reuses-material` | `material-reused-by` | the same material (passage, corpus, checkpoint), so results compare | Related line |
| `shares-listener` | `shares-listener` | the same human judge, so the results are not independent | Related line |

A kind whose far-end name is its own is **symmetric**: a link written from either end is the
same edge.

**Parent is not a link kind.** An item's parent is its sub-issue link, set from the item's
own parent ([kinds](repo-context-and-profiles.md#kinds)), never from a link record.
`supersedes` closes nothing: a register ends an item with its own event (a retire), and the
link only says which one to use now.

## The fold

A server folds a repo's link records, across every register its profile reads, in register
order, by these rules. Check L1 runs them on golden cases.

1. Only `link` and `unlink` lines with a `to` are item links. Every other line is ignored.
2. A `kind` outside the table is refused: `unknown-kind`.
3. Each end resolves to an item the repo's sources produce: the id itself, else the one
   item whose id is a source's id prefix followed by the name (a findings register names `F1`
   for the item `FINDING-F1`). An end that resolves to no item, or to more than one, is
   refused: `unknown-end`.
4. An item linked to itself is refused: `self-link`.
5. An edge is its kind and its two ends (unordered for a symmetric kind). A `link` makes or
   keeps it; repeating it changes nothing but the `why`, the latest of which stands. An
   `unlink` removes it, or is refused when it is not there: `no-such-link`.

A refused line is reported as a warning naming the register line, never applied, and never
fails the rest of the fold.

## On the mirrored issues

A sync that mirrors the items on issues MUST:

- write a **Related** section in each item's mirrored body that has an edge: one line per
  edge, the kind as this item reads it (its own kind for an edge from it, the far-end name
  for an edge to it), the other item's id and its issue reference (`#n`) when mirrored, and
  the `why`, clipped. Lines are in the table's kind order, then by the other id. Both ends
  carry the edge, so the inverse is visible without following GitHub's timeline.
- make each `depends-on` edge a native blocked-by link (the dependent item blocked by the
  other), through the same rules it uses for an item's dependencies: an edge to a closed
  item that has no issue is already satisfied and makes no link, and a sync removes only a
  blocker it made.
- keep the section stable: an unchanged set of edges plans no body edit.

A `rests-on` edge already shown in a finding's own citations list MAY be left out of that
finding's Related section; it still shows as `supports` on the far end.

## Writing a link

A tool that appends a `link` line for a caller MUST refuse, before it writes, a line the
fold would refuse (`unknown-kind`, `unknown-end`, `self-link`), a link that already stands
with the same kind and ends, and a link with no `why`. Registers fold one after another, so an
`unlink` cancels only a link written before it in the fold: the tool writes an `unlink` in
the register that holds the link, and refuses one whose link stands only in another. It records the caller as `by` and
the time as `t` with its offset, and refreshes both ends' issues after the write.

## Rendering the graph

A repo MAY render its links as an OKF bundle (an index with a diagram and one page per
item). A render reads the same records through the same fold as the sync, is never
hand-edited, and has a check mode that refuses a rendered bundle that differs from what
the records give. See [typed links](../knowledge/model/typed-links.md#the-graph-as-okf).
