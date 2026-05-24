# Validator Test Fixtures

End-to-end fixtures for `.github/scripts/validate-cip.py`. Each fixture is a single `README.md` in a descriptively-named directory.

## Layout

```
.github/tests/
  cip-valid/   CIP-valid-<description>/README.md     # expected to pass validation
  cip-invalid/ CIP-<description>/README.md            # expected to fail validation
```

## Run

```bash
bash .github/scripts/run-tests.sh                 # every fixture
bash .github/scripts/run-tests.sh minimal         # path-substring filter
bash .github/scripts/run-tests.sh cip-invalid     # just the failing set
```

Exit status is 0 if every fixture's actual outcome (pass/fail) matched its expected outcome; 1 otherwise. Output is one `PASS` / `FAIL` line per fixture, plus a `Passed: N  Failed: M` summary. On `FAIL`, the validator's stderr is shown indented.

First-time setup (install Python deps):

```bash
bash .github/scripts/setup-test-env.sh
```

## How the runner works

The validator enforces `directory-name == "CIP-NNNN"` (4-digit zero-padded match against the `CIP:` field). The fixtures here live in descriptively-named directories (`CIP-valid-minimal/`, `CIP-empty-authors/`, …) that would falsely trip that check. The runner copies each fixture into a temporary `CIP-NNNN/` directory (number taken from the fixture's frontmatter, `9999` for unassigned `?`) inside a per-fixture root before invoking the validator. Expected outcome is inferred from the parent directory:

- under `cip-valid/`   → expected `pass`
- under `cip-invalid/` → expected `fail`

### Companion folders

The validator's `Solution To` and body cross-reference checks look up sibling `CIP-NNNN/` and `CPS-NNNN/` folders at the repo root. To exercise these rules under controlled conditions, a fixture directory may contain additional empty subdirectories named like `CPS-0001/` or `CIP-0030/`. The runner copies them into the per-fixture root next to the temporary `CIP-NNNN/`, so the validator sees them as siblings. Companion folders are kept in git via a `.gitkeep` file inside each.

Examples:
- `cip-valid/CIP-valid-solution-to-single/CPS-0001/` makes `Solution To: [CPS-1]` resolve.
- `cip-invalid/CIP-solution-to-candidate-with-existing-folder/CPS-0001/` triggers the "candidate but folder exists" error for `Solution To: [CPS-1?]`.

## Adding a fixture

1. Pick the right category (`cip-valid/` or `cip-invalid/`).
2. Create `CIP-<short-description>/README.md`. Naming convention is `CIP-valid-<x>` for valid fixtures and `CIP-<x>` for invalid (matching the existing pattern).
3. If the fixture relies on a referenced CPS/CIP folder existing (or not existing), add a `CPS-NNNN/.gitkeep` / `CIP-NNNN/.gitkeep` companion folder under the fixture directory.
4. Make exactly one structural choice the test is about; everything else should be a clean baseline so the failure mode is unambiguous.
5. `bash .github/scripts/run-tests.sh <short-description>` to verify.

## CI

`.github/workflows/test-validators.yaml` runs the suite on push to `cip-validation-test`, on PRs that touch the validator or fixtures, and on `workflow_dispatch`.
