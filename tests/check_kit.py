#!/usr/bin/env python3
"""Checks for gtd-board-kit: size budgets, skill frontmatter, versions and local links.

Standard library only. Exit 0 when every check passes, 1 otherwise.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ["board-onboard", "board-pickup", "board-claim", "board-report", "board-needs-person"]
BOARD_BUDGET = 3000      # bytes; BOARD.md is read in full by every agent
SKILL_BUDGET = 6000      # bytes per SKILL.md
DESC_BUDGET = 1024       # characters; the Agent Skills limit for description
errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}
    out, section = {}, None
    for line in m.group(1).splitlines():
        if re.match(r"^\S[^:]*:\s*$", line):
            section = line.rstrip(":").strip()
            continue
        k, _, v = line.strip().partition(":")
        key = f"{section}.{k}" if line.startswith(" ") and section else k
        out[key.strip()] = v.strip()
    return out


version = (ROOT / "VERSION").read_text().strip()
if not re.fullmatch(r"\d+\.\d+\.\d+", version):
    fail(f"VERSION is not semver: {version!r}")

board = ROOT / "BOARD.md"
if board.stat().st_size > BOARD_BUDGET:
    fail(f"BOARD.md is {board.stat().st_size} bytes, over {BOARD_BUDGET}")
board_text = board.read_text()
for s in SKILLS:
    if f"`{s}`" not in board_text:
        fail(f"BOARD.md does not list {s}")

found = sorted(p.name for p in (ROOT / "skills").iterdir() if p.is_dir())
if found != sorted(SKILLS):
    fail(f"skills/ holds {found}, expected {sorted(SKILLS)} (update SKILLS and the installers)")

for s in SKILLS:
    path = ROOT / "skills" / s / "SKILL.md"
    if not path.exists():
        fail(f"{path.relative_to(ROOT)} missing")
        continue
    text = path.read_text()
    fm = frontmatter(text)
    if fm.get("name") != s:
        fail(f"{s}: frontmatter name is {fm.get('name')!r}")
    desc = fm.get("description", "")
    if not desc or len(desc) > DESC_BUDGET or "<" in desc or ">" in desc:
        fail(f"{s}: description missing, too long, or has angle brackets")
    if fm.get("metadata.version") is None:
        fail(f"{s}: no metadata.version")
    if path.stat().st_size > SKILL_BUDGET:
        fail(f"{s}: {path.stat().st_size} bytes, over {SKILL_BUDGET}")
    if "BOARD.md" not in text:
        fail(f"{s}: does not send the agent to BOARD.md")

for script in ("add-to-repo.sh", "add-to-repo.ps1"):
    body = (ROOT / "install" / script).read_text()
    for s in SKILLS:
        if s not in body:
            fail(f"install/{script} does not install {s}")

# PowerShell names are case-insensitive and functions beat executables, so a function
# named git would recurse on its own `& git` call .
for ps1 in (ROOT / "install").glob("*.ps1"):
    if re.search(r"(?im)^\s*function\s+git\b", ps1.read_text()):
        fail(f"install/{ps1.name}: a function named git shadows git.exe")

for md in ROOT.rglob("*.md"):
    for target in re.findall(r"\]\(([^)#\s]+)\)", md.read_text()):
        if "://" in target:
            continue
        if not (md.parent / target).exists():
            fail(f"{md.relative_to(ROOT)}: broken link {target}")

# The guard must pass on the whole tree: this repo is public.
import subprocess  # noqa: E402
guard = subprocess.run([sys.executable, str(ROOT / "tools" / "public_guard.py"), "--all"],
                       capture_output=True, text=True)
if guard.returncode != 0:
    fail("public_guard --all found private data:\n" + guard.stderr.strip())

# The guard must catch these shapes. Built at run time so the file itself stays clean.
LEAKS = ["tok " + "ghp_" + "a" * 30, "see " + "D:" + "\\work", "fixes " + "#" + "12",
         "board " + "acme/" + "4", "id " + "55" + "60276", "a" + "@" + "b.com",
         "/mnt/" + "project-files/x"]
for leak in LEAKS:
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "public_guard.py"), "--text"],
                       input=leak, capture_output=True, text=True)
    if r.returncode != 1:
        fail(f"public_guard missed a leak shape: {leak[:12]}...")
for trailer in ("Co-Authored-By: " + "ghp_" + "a" * 30,):
    r = subprocess.run([sys.executable, str(ROOT / "tools" / "public_guard.py"), "--text"],
                       input=trailer, capture_output=True, text=True)
    if r.returncode != 1:
        fail("public_guard lets a token through in a trailer")

if errors:
    print("\n".join(f"FAIL {e}" for e in errors))
    sys.exit(1)
print(f"ok: gtd-board-kit {version}, {len(SKILLS)} skills, BOARD.md {board.stat().st_size} bytes")
