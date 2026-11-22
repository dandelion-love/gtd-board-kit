"""Reference for an item's declared needs (server-spec/tools.md, Item needs), for check R12.
Standard library only. A server copies this and holds its copy to conformance/needs_cases.json.

    parse(body, size) -> {declared, graphics_gb, tools, longest_run_minutes,
                          longest_run_source, runs_anywhere, errors}

``body`` is the issue body; ``size`` the board Size (``XS`` to ``XL``) or None.
"""
from __future__ import annotations

import re

SIZE_RUN_MINUTES = {"XS": 15, "S": 60, "M": 240, "L": 1440, "XL": 4320}
KEYS = {"graphics memory": "graphics", "tools": "tools", "longest run": "run"}
TOOL = re.compile(r"[a-z0-9][a-z0-9._-]{0,39}\Z")
GB = re.compile(r"(\d+(?:\.\d+)?)\s*(?:gb)?\Z", re.I)
RUN = re.compile(r"(\d+(?:\.\d+)?)\s*(minutes?|mins?|m|hours?|hrs?|h|days?|d)\Z", re.I)
UNIT_MINUTES = {"m": 1, "h": 60, "d": 1440}


FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


def prose_lines(text: str) -> list[str]:
    """The lines outside fenced code blocks; an unclosed fence runs to the end."""
    out, fence = [], None  # the open fence's character and length
    for line in text.splitlines():
        m = FENCE.match(line)
        if fence is None:
            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):
                fence = (m.group(1)[0], len(m.group(1)))
                continue
            out.append(line)
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1] and not m.group(2).strip():
            fence = None
    return out


def section(body: str) -> list[str] | None:
    """The lines under the first ``## Needs`` heading, up to the next heading or rule; None if absent."""
    text = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)       # not a comment
    lines = prose_lines(text)
    for i, line in enumerate(lines):
        if re.fullmatch(r"##\s+Needs\s*", line):
            out = []
            for nxt in lines[i + 1:]:
                if nxt.startswith("#") or re.fullmatch(r" {0,3}-{3,}\s*", nxt):
                    break  # the next heading, or a rule (a server's sign-off starts with one)
                out.append(nxt)
            return out
    return None


def parse(body: str, size: str | None = None) -> dict:
    graphics = None
    tools: list[str] = []
    run = None
    errors: list[str] = []
    seen: set[str] = set()
    for raw in section(body) or []:
        line = re.sub(r"^\s*[-*]\s*", "", raw).strip()
        if not line or line.startswith("<!--"):
            continue
        key, sep, value = line.partition(":")
        name = KEYS.get(key.strip().lower())
        value = value.strip()
        if not sep or name is None:
            errors.append(f"unknown need {line[:60]!r}")
            continue
        if name in seen:
            errors.append(f"{key.strip()} is declared twice")
            continue
        seen.add(name)
        if name == "graphics":
            m = GB.match(value)
            if not m or float(m.group(1)) <= 0:
                errors.append(f"Graphics memory {value[:40]!r} is not a number of GB")
            else:
                graphics = float(m.group(1))
        elif name == "run":
            m = RUN.match(value)
            if not m or float(m.group(1)) <= 0:
                errors.append(f"Longest run {value[:40]!r} is not a number with a unit")
            else:
                run = int(round(float(m.group(1)) * UNIT_MINUTES[m.group(2)[0].lower()]))
        else:
            for t in (x.strip().lower() for x in value.split(",")):
                if not TOOL.match(t):
                    errors.append(f"tool {t[:40]!r} is not a tool name")
                elif t not in tools:
                    tools.append(t)
    declared = graphics is not None or bool(tools) or run is not None
    source = "declared" if run is not None else None
    if run is None and size in SIZE_RUN_MINUTES:
        run, source = SIZE_RUN_MINUTES[size], "size"
    return {"declared": declared, "graphics_gb": graphics, "tools": tools,
            "longest_run_minutes": run, "longest_run_source": source,
            "runs_anywhere": not declared, "errors": errors}
