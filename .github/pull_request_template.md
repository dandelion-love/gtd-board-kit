## What

<!-- What changes, and why. -->

## Checks

- [ ] `python3 tests/check_kit.py` passes
- [ ] `python3 tools/public_guard.py --all` is clean (this repository is public)
- [ ] `VERSION` and the changed skills' `metadata.version` are bumped
- [ ] If `server-spec/` changed: the check table (`server-spec/conformance.md`) and the
      runner (`conformance/`) changed with it, or a commit carries `Conformance-unchanged: <reason>`
      (`python3 tools/spec_pair.py` says which)
