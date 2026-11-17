# Shared resource checkout

Part of `board-claim`; read `.gtd/kit/BOARD.md` first. Follow this for a lane or a
one-off job that needs a resource another participant can use. A work-item claim and
a resource checkout are separate. A local process check or a free-looking device is
not an atomic reservation and does not authorize a start.

1. Discover the resource tools and their current input schemas through the MCP server.
   Use `resource_list` or `resource_get` to find the registered resource and
   `resource_checkout_get` to inspect its state. If the server, required tools, or
   resource is unavailable, stop the resource-dependent work and report the block.
   A resource owner or authorized administrator may use `resource_register` to add
   one and `resource_update` to set a hold. Do not register or lift a hold without
   that authority. Inspection does not grant use.
2. Before requesting a checkout, generate the recovery proof required by the server
   and keep it in session-private secure storage, together with a stable request ID.
   Do not put proof, capability or credentials in a board record, log or shared file.
   Use `resource_acquire` for an immediate checkout, or `resource_enqueue` and bounded
   `resource_wait` for an ordered wait, following the discovered schemas. Start only
   after receiving an active committed grant and only through the participating
   launcher and workload boundary configured for that resource. A timeout is not a
   grant and does not cancel a wait. A lane tick need not wait: report the pending
   request and resume it on a later tick with the same private proof.
3. Keep the capability private and renew with `resource_renew` before expiry. On a
   lost response, retry or use `resource_wait_recover` with the same request ID and
   proof; a different session under the same principal is not proof of possession.
   `resource_wait_cancel` cancels a pending wait, not an already committed grant;
   check its result and recover any grant before acting. Never issue a fresh request
   merely because a reply was lost.
4. After the workload and its participating children have ended, call
   `resource_release`. Release, expiry, a failed probe, an unknown workload or lost
   continuity does not prove the resource free. Only the owner or an authorized
   administrator may request `resource_recover`, using the operation ID from
   `resource_checkout_get`; the configured trusted verifier must seal and verify the
   operation. A failed or unavailable verifier leaves it unavailable. A hold remains
   in force until an authorized person lifts it. Do not bypass any refusal.

The checkout coordinates only participating launchers and the workload boundary their
trusted verifier covers. It does not fence other launchers, delegated work, or a
physical device by itself. Identify unconverted launchers before relying on exclusion;
when their activity cannot be ruled out, do not start a conflicting job.
