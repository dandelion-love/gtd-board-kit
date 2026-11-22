"""Reference for the app board's columns (server-spec/app-board.md), for check AB1.
Standard library only. A server copies this and holds its copy to conformance/app_columns_cases.json.

    column_for(status, mapping=None) -> one of COLUMNS
    check_mapping(mapping)           -> {ok, error}

``mapping`` is a profile's ``app_columns``: Board Status option -> column. Without one the
default (the ``software`` profile's options) applies; a Status with no entry is ``other``,
never dropped.
"""
from __future__ import annotations

COLUMNS = ("waiting", "ready", "in_progress", "needs_you", "done", "other")
DEFAULT_MAPPING = {"Backlog": "waiting", "Blocked": "waiting", "Ready": "ready",
                   "In Progress": "in_progress", "In Review": "in_progress",
                   "Needs owner": "needs_you", "Done": "done"}


def check_mapping(mapping) -> dict:
    if not isinstance(mapping, dict) or not mapping:
        return {"ok": False, "error": "mapping is not a non-empty object"}
    for k, v in mapping.items():
        if not isinstance(k, str) or not k.strip() or v not in COLUMNS or v == "other":
            return {"ok": False, "error": f"{k!r} maps to {v!r}, which is not a column"}
    return {"ok": True, "error": None}


def column_for(status, mapping: dict | None = None) -> str:
    table = mapping if mapping else DEFAULT_MAPPING
    key = " ".join(status.split()).lower() if isinstance(status, str) else ""
    for name, col in table.items():
        if " ".join(name.split()).lower() == key and key:
            return col
    return "other"
