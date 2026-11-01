#!/usr/bin/env python3
"""Spec changes travel with conformance changes.

A change under server-spec/ must also change the checks (server-spec/conformance.md or
conformance/), or say why not in a commit trailer:

    Conformance-unchanged: <reason, e.g. wording only>

Usage:
    python3 tools/spec_pair.py                    # this branch against origin/main
    python3 tools/spec_pair.py --base <ref>       # this branch against another base
    python3 tools/spec_pair.py --range <a>..<b>   # a commit range (the pre-push hook uses this)

Standard library only. Exit 0 when paired or excused, 1 when not, 2 on a git error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys

TRAILER = re.compile(r"^Conformance-unchanged:\s*\S", re.MULTILINE)


def git(*args: str) -> str:
    return subprocess.run(["git", *args], capture_output=True, text=True, check=True).stdout


def verdict(files: list[str], messages: str) -> tuple[bool, str]:
    spec = sorted(f for f in files if f.startswith("server-spec/") and f != "server-spec/conformance.md")
    checks = [f for f in files if f == "server-spec/conformance.md" or f.startswith("conformance/")]
    if not spec:
        return True, "no server-spec change"
    if checks:
        return True, f"spec and checks change together ({len(spec)} spec, {len(checks)} check files)"
    if TRAILER.search(messages):
        return True, "spec change excused by a Conformance-unchanged trailer"
    return False, ("server-spec/ changed without a conformance change:\n  " + "\n  ".join(spec) +
                   "\nAdd or update the checks (server-spec/conformance.md and conformance/), or, for a "
                   "change that cannot affect conformance,\nadd a commit trailer "
                   "'Conformance-unchanged: <reason>'.")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--base", default="origin/main", help="compare this branch with REF (default origin/main)")
    g.add_argument("--range", help="check the commits in A..B")
    a = ap.parse_args(argv)
    span = a.range or f"{a.base}...HEAD"
    try:
        files = git("diff", "--name-only", span).split()
        messages = git("log", "--format=%B", span.replace("...", ".."))
    except subprocess.CalledProcessError as e:
        print(f"spec_pair: git failed: {e.stderr.strip()}", file=sys.stderr)
        return 2
    ok, why = verdict(files, messages)
    print(("ok: " if ok else "spec_pair: ") + why, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
