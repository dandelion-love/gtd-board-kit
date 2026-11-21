"""Reference for the intake check's status rules (server-spec/tools.md, The intake check), for
checks I6 to I9. Standard library only. A server copies this and holds its copy to
conformance/intake_check_cases.json.

    derive(records, created, since, mode) -> {status, grandfathered, held, label}

`records` are the trusted check records in comment order (each has `result`); `created` and
`since` are comparable times (the fixtures use minutes); `mode` is `watch`, `enforce` or
anything else (read as `watch`).
"""
from __future__ import annotations

RESULTS = ("pass", "needs-more", "decline")
MODES = ("watch", "enforce")


def derive(records: list[dict], created: float, since: float | None, mode: str | None) -> dict:
    latest = next((r for r in reversed(records) if r.get("result") in RESULTS), None)
    status = latest["result"] if latest else "unchecked"
    mode = mode if mode in MODES else "watch"
    grandfathered = status == "unchecked" and since is not None and created < since
    held = mode == "enforce" and status in ("needs-more", "decline")
    return {"status": status, "grandfathered": grandfathered, "held": held,
            "label": held, "pickable": not held}


def valid(result: str, clear: bool, small: bool, fits: bool, note: str | None) -> str | None:
    """The rule a call breaks, or None when it is writable."""
    if result not in RESULTS:
        return "result"
    if result == "pass" and not (clear and small and fits):
        return "pass-needs-all-three"
    if result == "needs-more" and (fits is not True or (clear and small)):
        return "needs-more-shape"
    if result == "decline" and fits:
        return "decline-needs-no-fit"
    if result != "pass" and not (note or "").strip():
        return "note-required"
    return None
