# Experiment evidence discovery

`experiment-evidence:1` is optional. When a server names it in `whoami.capabilities`,
it MUST expose the read-class `experiment_evidence_get` tool. Its required inputs are
`repo`, `id`, `result_line_sha256` (64 lowercase hex digits) and `ref` (a full immutable
40-hex repository commit). The server applies the normal repo authorization before
reading. Resolve that commit and return its full hash; no working tree, branch tip or
implicit latest result is a substitute.

Read all original result record lines for the selected item at that commit, in the
register's configured file or page layout. `result_line_sha256` hashes the exact UTF-8
line bytes without the terminating newline; it does not hash reformatted JSON. Refuse
zero or multiple matches, an invalid hash, an unreadable commit, or a matched line whose
id or event is wrong. Do not silently choose a duplicate or a different result.

The response carries `repo`, `id`, resolved `ref`, `result_line_sha256`, `verdict`,
`result_data` (the complete original data object or null), `evidence_status`, and
`review_evidence`. `evidence_status` is `present`, `legacy` or
`empty-void`. For `present`, return the exact `data.review_evidence` object; for the
other statuses return null. An empty VOID has no data and no finding; a legacy result
has no evidence envelope. A populated VOID is handled as any other result. A malformed
present envelope MUST be refused rather than treated as legacy. Validate its fields,
source identity, canonical receipt hash and its binding to the result data as specified
by the golden cases. Canonical JSON is UTF-8, sorted keys, no insignificant whitespace,
unescaped Unicode and no non-finite numbers. Inputs, outputs and references remain in
the hash-pinned bundle, not the response.

An envelope has exactly `receipt` and `receipt_sha256`. Receipt version 1 uses method
`immutable-bundle-local-python-replay-v1`; it holds `uri`, `generation`,
`bundle_sha256`, `manifest_sha256`, `replay_sha256`, `result_sha256` and an offset-aware
`verified_at`. The source is a `gs://` object with immutable decimal generation or a
`git:` repository path with a full commit. These are attestations, not proof of
availability, privacy, authorship, or actual replay. The server MUST NOT fetch the
artifact, execute a scorer, assert verification occurred, or return credentials.
An authorized reviewer retrieves pinned bytes and runs a trusted scorer on an
appropriate host. Existing item-level artifact links remain contextual; the server
MUST NOT assign them to a specific result or infer a receipt from them.

These requirements do not add a generic result writer: the existing
`written-on-the-host` refusal for experiment results remains in force. Older records
and operational failures remain readable. Repositories may adopt further local gates;
this discovery interface makes no new claim that every result has evidence.
