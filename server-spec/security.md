# 07. Security

These hold for every deployment. Each has a conformance check in [conformance](conformance.md).

## Identity

- S1. The principal comes only from the verified bearer token. No tool takes an identity,
  author or `by` argument that is used as identity.
- S2. A connector sign-in is gated by an operator allowlist of identities.
- S3. Approvers are matched by stable account ids. No MCP tool approves, denies or revokes
  a join.
- S4. Joined-agent tokens are opaque, at least 256 bits, stored only as hashes, looked up
  on every call, and never accepted by another verifier.
- S5. Refresh tokens are single use; a reused one revokes the whole agent.

## Reach

- S6. Repo and board allowlists fail closed and are checked before any GitHub call.
- S7. The preset fence hides and refuses tools above the caller's preset, in one place.
- S8. The caller's MCP token is never forwarded to GitHub. No tool result contains a
  GitHub credential, a server secret, or a token hash.
- S9. Webhook and other outbound URLs a tool can set are checked against an operator host
  allowlist; empty means refuse.

## Records and content

- S10. `issue_comment` and every free-text tool refuse a body carrying a record marker.
  `pr_open` also refuses a body carrying a `gtd-pr` marker.
- S11. Text from issues, comments and boards is data. The server never follows
  instructions found in it, and tool descriptions say so where an agent might.
- S12. Free-text inputs are length-capped and refused, not silently truncated, when too
  long. Record JSON escapes `<` and `>`.
- S13. When record authors are configured, records by anyone else are ignored.

## Operation

- S14. Logs carry the principal, the tool, the repo or board and the outcome. They never
  carry a bearer token, refresh token, GitHub token, cookie or secret.
- S15. The operator can stop every joined agent with one configuration change (no
  approvers), and from the browser with revoke-all.
- S16. Tools that delete (an item, a field, a view, a workflow, a webhook) are `full`
  class and refuse without an explicit confirmation argument where the effect is not
  reversible.
- S17. The approver pages set `HttpOnly`, `Secure`, `SameSite=Lax` cookies scoped to
  `/join` and use CSRF tokens on every form.
