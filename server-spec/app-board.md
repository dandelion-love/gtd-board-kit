# App board

`app_board` is one read-only call that gives the unified app everything its board screen
needs: five columns and a catch-all, each item's worker and time left, and the items waiting
for the signed-in person. It is optional and additive.

## Arguments and result

`app_board` (read): `project?` (the board; the server's default if it has one),
`repo?` (limit to one repo). It returns:

- `columns`: an object with the keys `waiting`, `ready`, `in_progress`, `needs_you`, `done`
  and `other`, each a list of items `{repo, number, title, status, url, labels}`. Every
  item on the board appears in exactly one column.
- `counts`: the length of each column, same keys.
- `needs_you_count`: how many items wait for the caller (below).
- `truncated`: true when the board had more items than the call returned.

A column is chosen from the item's board **Status**. The profile supplies the mapping as
`app_columns` (Status option to column name) in `profile_get`; matching ignores case and
extra spaces. A profile without one gets the default:

| Status | Column |
| --- | --- |
| Backlog, Blocked | `waiting` |
| Ready | `ready` |
| In Progress, In Review | `in_progress` |
| Needs owner | `needs_you` |
| Done | `done` |

A Status with no mapping, and an item with no Status, goes under `other`; nothing is ever
dropped. A mapping may target only `waiting`, `ready`, `in_progress`, `needs_you` and `done`
(not `other`), and an empty or invalid one is refused when the profile is loaded. Check AB1
holds a server's mapping to [app_columns_cases.json](../conformance/app_columns_cases.json);
the reference is [app_columns.py](../conformance/app_columns.py).

## Running items and the caller's items

- An item in `in_progress` that has a live claim carries `worker` (the principal that holds
  it) and `lease_seconds_left` (0 or more). One with no live claim carries both as null.
- An item whose labels include the `needs:<owner_needs>` label of the profile is
  **waiting for you** when the caller is the owner: it is marked `waiting_for_you: true` and
  counted in `needs_you_count`. Another person's `needs:*` items are never marked or counted.
  The server decides who the owner is from the signed-in principal, never from an argument.
- The call writes nothing and returns no credential, token or secret.
