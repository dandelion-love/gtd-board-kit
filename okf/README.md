# OKF, pinned by the kit

The kit adopts the **Open Knowledge Format (OKF)**, an open format for knowledge as a
directory of markdown files with YAML frontmatter, and pins the version every repo that
uses the kit follows.

| File | What |
| --- | --- |
| `SPEC.md` | The OKF specification, copied unchanged from the upstream commit in `PIN.json` |
| `LICENSE.md` | Its license (Apache 2.0), copied unchanged |
| `PIN.json` | Upstream repository, the pinned commit, and the `okf_version` it specifies |

Upstream: https://github.com/GoogleCloudPlatform/open-knowledge-format. The older copy
under `knowledge-catalog/okf` is a frozen snapshot; do not pin to it.

## Using it in a work repo

Knowledge docs in a repo that pulls in the kit follow `.gtd/kit/okf/SPEC.md`: declare
`okf_version` in the bundle's root `index.md` and lint with
`python3 .gtd/kit/tools/okf_lint.py <bundle-dir>`. The `okf-knowledge` skill has the
authoring rules. The repo gets a newer OKF by moving its kit pin, never by editing
these files.

## Moving the pin (kit maintainers)

1. Read the upstream changelog section of the new `SPEC.md`.
2. Copy `SPEC.md` and `LICENSE.md` from the new upstream commit unchanged, and update
   `PIN.json` (`commit`, `okf_version`, `checked`).
3. Update `skills/okf-knowledge`, `tools/okf_lint.py` and the kit's own `knowledge/`
   bundle for anything the new version changes, run `python3 tests/check_kit.py`, and
   bump the kit `VERSION`.
