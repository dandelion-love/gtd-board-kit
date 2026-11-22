"""Reference for a machine's card and for whether an item fits it (server-spec/machine-fit.md),
for checks MF1 and MF2. Standard library only. A server copies this and holds its copy to
conformance/machine_fit_cases.json.

    check_card(card)                  -> {ok, card, fields}
    fit(card, needs, speed_factor=1)  -> {fits, reasons}

``card`` is what a machine says it has: ``graphics_gb``, ``free_storage_gb``, ``tools`` and
``speed_minutes`` (minutes the machine takes for the fixed reference job). ``needs`` is an
item's ``needs`` as ``item_get`` returns it (server-spec/tools.md, Item needs).
"""
from __future__ import annotations

import re

TOOL = re.compile(r"[a-z0-9][a-z0-9._-]{0,39}\Z")
FIELDS = ("graphics_gb", "free_storage_gb", "tools", "speed_minutes")
MAX_TOOLS = 50


def _number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and value == value \
        and value not in (float("inf"), float("-inf"))


def check_card(card) -> dict:
    """Validate a card. Every field is required. ``fields`` names each field that is missing,
    not a number, out of range or unknown; ``card`` is the normalised card when ``ok``."""
    if not isinstance(card, dict):
        return {"ok": False, "card": None, "fields": ["card"]}
    bad = [k for k in sorted(card) if k not in FIELDS]  # a stray key could carry a credential
    for k in ("graphics_gb", "free_storage_gb"):
        if not _number(card.get(k)) or card[k] < 0:
            bad.append(k)
    if not _number(card.get("speed_minutes")) or card["speed_minutes"] <= 0:
        bad.append("speed_minutes")
    tools = card.get("tools")
    clean: list[str] = []
    if not isinstance(tools, list) or len(tools) > MAX_TOOLS:
        bad.append("tools")
    else:
        for t in tools:
            t = t.strip().lower() if isinstance(t, str) else None
            if t is None or not TOOL.match(t):
                bad.append("tools")
                break
            if t not in clean:
                clean.append(t)
    bad = sorted(set(bad), key=lambda k: (FIELDS.index(k) if k in FIELDS else 99, k))
    if bad:
        return {"ok": False, "card": None, "fields": bad}
    return {"ok": True, "fields": [], "card": {
        "graphics_gb": float(card["graphics_gb"]), "free_storage_gb": float(card["free_storage_gb"]),
        "tools": clean, "speed_minutes": float(card["speed_minutes"])}}


def _n(x) -> str:
    x = float(x)
    return str(int(x)) if x == int(x) else f"{x:g}"


def fit(card: dict, needs: dict, speed_factor: float = 1.0) -> dict:
    """Does an item with these ``needs`` fit a machine with this (valid) ``card``? An item that
    runs anywhere always fits: a Size default is not a declared need. Reasons are in the order
    graphics, tools (in the item's order), run."""
    if needs.get("runs_anywhere"):
        return {"fits": True, "reasons": []}
    reasons = []
    g = needs.get("graphics_gb")
    if g is not None and card["graphics_gb"] < g:
        reasons.append(f"needs {_n(g)} GB graphics, machine has {_n(card['graphics_gb'])} GB")
    for t in needs.get("tools") or []:
        if t not in card["tools"]:
            reasons.append(f"needs tool {t}, machine does not list it")
    run = needs.get("longest_run_minutes")
    if run is not None and card["speed_minutes"] * speed_factor > run:
        reasons.append(f"longest run {_n(run)} minutes, machine needs "
                       f"{_n(card['speed_minutes'] * speed_factor)} minutes for the reference job")
    return {"fits": not reasons, "reasons": reasons}
