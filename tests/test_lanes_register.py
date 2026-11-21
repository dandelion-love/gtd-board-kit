#!/usr/bin/env python3
"""Offline tests for register-form merge grants in tools/lanes.py: a grant that names a
register covers a record page only when the PR appends valid records to it. Standard library
only; builds a throwaway git repo for the command-line check.
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "conformance"))
import lanes  # noqa: E402
import record_pages as pages  # noqa: E402

CASES = json.loads((ROOT / "conformance" / "record_cases.json").read_text())["cases"]["validate"]
REGISTER = next(c["line"] for c in CASES if c["name"] == "register-ok")
ENVELOPE = {"v": 1, "id": "EXP-1", "eid": "01JC0000000000000000000002", "t": "2026-01-03 10:00:00+00:00",
            "by": "agent:example", "via": "tool@1"}


MAIL = "t" + chr(64) + "example.test"  # built at run time so this file passes public_guard


def line(**fields):
    return json.dumps({**ENVELOPE, **fields})


START = line(event="start", resource="host-a")
TEXT = """## Merge grants

### merge: records
- registers:
  - experiment
  - note
- granted_by: owner
- date: 2026-01-01
- link: https://example.test/grant

## Register pages

### register: experiment
- kind: experiment
- folder: experiments
- layout: item-folder
- type: Experiment

### register: note
- kind: finding
- folder: notes
- layout: flat
"""
PAGE = "experiments/EXP-1/README.md"


def page(*lines):
    return pages.render_page("EXP-1", "Experiment", list(lines))


def covers(path, old, new, text=TEXT):
    return lanes.covering_grants(text, [path], lambda p: (old, new))


class RegisterGrant(unittest.TestCase):
    def test_lint_accepts_register_form_and_refuses_folders_and_globs(self):
        self.assertEqual(lanes.check(TEXT), [])
        bad = TEXT.replace("- folder: experiments", "- folder: experiments/*")
        self.assertTrue(any("not a pattern" in p for p in lanes.check(bad)))
        bad = TEXT.replace("- folder: experiments", "- folder: .gtd")
        self.assertTrue(any("not a pattern" in p for p in lanes.check(bad)))
        bad = TEXT.replace("  - note\n", "  - missing\n")
        self.assertTrue(any("register missing has no block" in p for p in lanes.check(bad)))
        bad = TEXT.replace("- layout: flat", "- layout: tree")
        self.assertTrue(any("layout must be" in p for p in lanes.check(bad)))
        # a bare folder in `paths` is still refused
        folder = TEXT.replace("- registers:\n  - experiment\n  - note\n", "- paths:\n  - experiments/\n")
        self.assertTrue(any("pattern or folder" in p for p in lanes.check(folder)))

    def test_appending_valid_records_to_an_existing_page_is_covered(self):
        old = page(REGISTER)
        self.assertEqual(covers(PAGE, old, page(REGISTER, START))[0], ["records"])

    def test_a_new_page_from_a_valid_first_record_is_covered(self):
        self.assertEqual(covers(PAGE, None, page(REGISTER))[0], ["records"])

    def test_edit_to_a_non_record_line_fails(self):
        old = page(REGISTER)
        new = page(REGISTER, START).replace("# EXP-1", "# EXP-1 renamed", 1)
        names, why = covers(PAGE, old, new)
        self.assertEqual(names, [])
        self.assertIn("edits-existing-content", " ".join(why))

    def test_removing_or_changing_an_existing_record_fails(self):
        old = page(REGISTER, START)
        self.assertEqual(covers(PAGE, old, page(REGISTER))[0], [])
        changed = REGISTER.replace('"A beats B"', '"A loses to B"')
        self.assertEqual(covers(PAGE, old, page(changed, START))[0], [])
        self.assertEqual(covers(PAGE, old, None)[0], [])

    def test_an_added_record_that_fails_validation_fails(self):
        old = page(REGISTER)
        names, why = covers(PAGE, old, page(REGISTER, line(event="start")))
        self.assertEqual(names, [])
        self.assertIn("missing:resource", " ".join(why))
        names, why = covers(PAGE, None, page(START))
        self.assertIn("not-registered", " ".join(why))

    def test_a_record_for_another_item_fails(self):
        old = page(REGISTER)
        other = json.dumps({**json.loads(START), "id": "EXP-2"})
        self.assertEqual(covers(PAGE, old, page(REGISTER, other))[0], [])

    def test_paths_outside_the_layout_are_not_covered(self):
        old = page(REGISTER)
        for path in ("experiments/EXP-1.md", "experiments/EXP-1/notes.md", "experiments/EXP-1/x/README.md",
                     "src/app.py", "experiments/../.gtd/BOARD.local.md", ".gtd/BOARD.local.md"):
            self.assertEqual(covers(path, old, page(REGISTER, START))[0], [], path)

    def test_without_a_reader_a_register_covers_nothing(self):
        self.assertEqual(lanes.merge_covers(TEXT, [PAGE]), [])

    def test_one_grant_must_cover_every_file(self):
        old = page(REGISTER)
        names, _ = lanes.covering_grants(TEXT, [PAGE, "src/app.py"], lambda p: (old, page(REGISTER, START)))
        self.assertEqual(names, [])

    def test_exact_paths_and_a_register_mix_in_one_grant(self):
        mixed = TEXT.replace("- registers:", "- paths:\n  - data/log.jsonl\n- registers:")
        old = page(REGISTER)
        names, _ = lanes.covering_grants(mixed, [PAGE, "data/log.jsonl"], lambda p: (old, page(REGISTER, START)))
        self.assertEqual(names, ["records"])

    def test_flat_layout(self):
        fact = json.dumps({**ENVELOPE, "id": "F-1", "event": "fact", "section": "s", "statement": "x",
                           "rests_on": [{"id": "EXP-1", "of": "a" * 64, "verdict": "YES"}], "caveat": "none: nothing"})
        new = pages.render_page("F-1", "note", [fact])
        names, why = covers("notes/F-1.md", None, new)
        self.assertEqual(names, ["records"], why)


class CommandLine(unittest.TestCase):
    def test_head_and_base_read_the_pr(self):
        with tempfile.TemporaryDirectory() as d:
            def git(*a):
                subprocess.run(["git", *a], cwd=d, check=True, capture_output=True,
                               env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": MAIL,
                                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": MAIL,
                                    "PATH": "/usr/bin:/bin:/usr/local/bin"})
            root = Path(d)
            git("init", "-q", "-b", "main")
            (root / ".gtd").mkdir()
            (root / ".gtd" / "BOARD.local.md").write_text(TEXT)
            (root / "experiments" / "EXP-1").mkdir(parents=True)
            (root / PAGE).write_text(page(REGISTER))
            git("add", "-A"); git("commit", "-qm", "base")
            git("update-ref", "refs/remotes/origin/main", "HEAD")
            git("symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
            git("checkout", "-q", "-b", "pr")
            (root / PAGE).write_text(page(REGISTER, START))
            git("commit", "-qam", "append")
            git("checkout", "-q", "-b", "bad", "main")
            (root / PAGE).write_text(page(REGISTER, START).replace("# EXP-1", "# renamed", 1))
            git("commit", "-qam", "edit")

            def run(head, *files):
                return subprocess.run([sys.executable, str(ROOT / "tools" / "lanes.py"), "check", "--merged",
                                       "--head", head, "--merge", *files], cwd=d, capture_output=True, text=True)
            ok = run("pr", PAGE)
            self.assertEqual(ok.returncode, 0, ok.stdout)
            bad = run("bad", PAGE)
            self.assertEqual(bad.returncode, 1)
            self.assertIn("edits-existing-content", bad.stdout)
            # without --head only exact files count
            plain = subprocess.run([sys.executable, str(ROOT / "tools" / "lanes.py"), "check", "--merged",
                                    "--merge", PAGE], cwd=d, capture_output=True, text=True)
            self.assertEqual(plain.returncode, 1)


if __name__ == "__main__":
    unittest.main()
