# Notifications

How a server turns an agent's ask into **one** notification for the right person, and
nothing else. The agent-side rule is [BOARD.md](../BOARD.md) rule 7; the reasons are in the
decision [notify only when a person must act](../knowledge/decisions/notify-only-when-a-person-must-act.md).
This is an optional group ([tools](tools.md#optional-groups)): a server that offers it
lists `notify_get` in `tools/list` and passes the N checks in
[conformance](conformance.md#notifications-when-offered).

Why the server and not the agent: an agent can forget the mention, write it twice, or
write it under an identity GitHub will not notify (GitHub never notifies anyone of their
own actions). The server sees every ask, knows which identity it writes as, and can keep
one ping per ask. So when the group is offered, agents never write the mention themselves.

## Three pushes, nothing else

A server in this group notifies a person for exactly these, and for nothing else:

| Reason | Trigger | Carried by |
| --- | --- | --- |
| `ask` | `item_report` with `attention` and a `needs` the repo maps to a person | One ping comment on the item ([below](#the-ping-comment)) |
| `pr-ready` | `pr_open` with `draft` false | A review request on the PR ([below](#review-requests-from-pr_open)) |
| `stop` | `item_report` with `state=dropped` and `attention` | The same ping comment as an ask |

A claim, renew, release, progress report, done report, comment, label, Status change, new
issue or retry never notifies anyone. New issues wait in the repo's views.

## The map

The repo says who each `needs` value means in `.github/gtd-context.json`
([repo context](repo-context-and-profiles.md#githubgtd-contextjson)), under `notify`:

```json
{
  "profile": "software",
  "notify": {
    "mentions": {"owner": "octo-owner"},
    "push": "none",
    "new_issues": "view"
  }
}
```

| Key | Meaning |
| --- | --- |
| `mentions` | `needs` value (without the `needs:` prefix) to a GitHub login, without `@`. A value missing here pings nobody |
| `push` | The louder channel that copies the pushes: `none` (default) or `web-push` ([push copy](#push-copy)). It is repo-wide on purpose: one owner per repo is the common case, and a repo with several people gives each their own subscriptions on the deployment's subscribe page |
| `new_issues` | `view` (default: they wait in the Inbox view), `digest` or `watch`. The server acts only on `digest`, and only if it offers a digest; `watch` is the owner's own GitHub setting |

The server reads the file through the GitHub API, as for the profile. It MUST NOT trust
the map for authorization: a login in the map is only whom to mention.

## Which identity pings

A ping is written as **`ping_as`**: an identity the server can write as that is **not** the
login it mentions. The default is the server's GitHub App installation (a `[bot]` account),
the same credential `pr_open` uses. A server that writes claim records under a person's
own account (a deployment choice; see `via_server` in [new activity](tools.md#new-activity))
still writes the ping as the App.

When the only identity that can write is the person to be notified, the server MUST NOT
post the mention: the ping result says `no-identity`, `notify_get` lists a warning, and the
ask still stands on the board.

## `notify_get`

| Tool | Class | Arguments | Returns |
| --- | --- | --- | --- |
| `notify_get` | read | `repo`, `number?` | `repo`, `mentions`, `push`, `new_issues`, `ping_as`, `warnings`, and with `number`: `pings` |

- `mentions`, `push`, `new_issues` are the map as read (defaults filled in); an absent
  `notify` key gives `mentions` `{}`.
- `ping_as` is the login the server pings as (for example `example-app[bot]`), or null when
  it has no identity other than the mapped person's.
- `warnings` names each mapped login the server cannot ping (`no identity other than
  @octo-owner can write`) and each `needs` value in the map that the profile does not have.
- `pings` (with `number`) lists the item's trusted pings, oldest first, each `{key, to,
  reason, url, author, created_at}`, where `author` is the comment's author login as GitHub
  returns it. Only comments written as `ping_as` count; a pasted marker from anyone else is
  ignored, as in the claim fold.

## The ping comment

On an `item_report` that carries `attention` (an ask, or a stop with `state=dropped`), the
server first writes the claim record as usual, then, when `needs` maps to a login and
`ping_as` exists, posts **one separate comment** as `ping_as`:

```text
@octo-owner: Which storage engine should the cache use? https://github.com/owner/repo/issues/N#issuecomment-M

---
<sub>gtd-sign · agent:example · worker · ping · session build-3 · 2026-01-01T12:00:00Z</sub>

<!-- gtd-ping v1 {"for": "octo-owner", "key": "N:owner:3f9a0c1d2e4b5a69", "reason": "ask", "record": "https://github.com/owner/repo/issues/N#issuecomment-M", "t": "2026-01-01T12:00:00Z", "v": 1} -->
```

- The first line is `@<login>: `, then the first line of `attention` cut to 200
  characters, then the URL of the record the report wrote. Nothing else mentions anyone.
- It is a **new comment**, never an edit: GitHub does not notify for a mention added by an
  edit.
- It ends with a [sign-off](sign-offs.md) with `act` `ping`, then the `gtd-ping` marker,
  which stays last. The marker's JSON follows the
  [record rules](claim-records.md#record-format): `<` and `>` escaped, keys sorted.
- `key` is `<number>:<needs>:<h>`, where `<h>` is the first 16 hex characters of the
  SHA-256 of `attention` with runs of whitespace collapsed to one space and the ends
  trimmed. It is the same key a push copy uses as its `tag` and `Topic`.
- **One ping per ask.** Before posting, the server reads the item's trusted pings. If one
  has the same `key`, it posts nothing. A changed question (new text, or a new `needs`) is
  a new key and pings again.
- The ping is not a claim record: the fold ignores it, and `activity_since` leaves it out.
- A failed ping write is a warning; the record stands.

`item_report` returns, beside its usual fields, `ping`:

| `ping.reason` | When | `posted` |
| --- | --- | --- |
| `posted` | A new ping was written | true, with `to`, `as`, `url`, `key` |
| `unchanged` | A trusted ping with this key exists | false, with `url` of that one |
| `no-map` | `needs` maps to nobody | false |
| `no-identity` | No identity other than the mapped login can write | false, with `to` |
| `failed` | The write failed (also a warning) | false |

An `item_report` without `attention` returns `ping` null and posts nothing.

## Review requests from `pr_open`

When the group is offered, a non-draft `pr_open` also requests a review, as the App that
authored the PR, from the login the map gives the profile's `owner_needs`. It returns
`review_requested` (the login) or null with a warning saying why (no map, or GitHub refused).
A draft requests no review; marking it ready later is the person's or a later tool's act.
The review request is the `pr-ready` push: the server posts no ping comment for it. Its
key is `<pr number>:review:<h>`, where `<h>` is the first 16 hex characters of the PR's
head commit SHA, so a new push to the branch does not request again on its own (GitHub
keeps the request until the reviewer acts).

## Push copy

With `push` set to `web-push`, the server also sends each posted ping (never an
`unchanged` one) **and each review request `pr_open` makes** to the owner's subscribed
devices. A server that offers this:

- sends a payload with `title` (the repo and item), `body` (the ping's first line without
  the URL, at most 100 words; for a review request, the PR title), `navigate` (the item's
  or PR's URL), `reason` (`ask`, `pr-ready` or `stop`, the names of the table
  [above](#three-pushes-nothing-else)), and `tag` set to the ping's or review request's
  `key`; and sets the Web Push `Topic` header to a URL-safe form of the same key, with
  `Urgency: high` for an ask or stop and `normal` for `pr-ready`;
- offers at most these actions: **Open** (navigate), **Snooze** (one reminder later) and
  **Answer** (opens a page where the owner, signed in, writes the answer as themselves);
- puts no token, secret or one-time code in the payload, the action URL or the page URL;
- sends at most one reminder per key, at the owner's next sitting, and none for a key
  that a person has answered, whose `needs:*` label was removed, or whose PR was reviewed,
  merged or closed.

The subscribe page, the answer page and their sign-in are the deployment's. The ping on
GitHub stays the record; a push is only a copy.

## What a server must not do

- Add a mention of its own anywhere but a ping (records and PR bodies carry the caller's
  text as given).
- Ping as the person it mentions.
- Ping twice for one key, or ping for anything outside the three reasons.
- Remove a `needs:*` label or answer an ask for the person.
