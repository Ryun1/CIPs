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

The validator enforces `directory-name == "CIP-NNNN"` (4-digit zero-padded match against the `CIP:` field). The fixtures here live in descriptively-named directories (`CIP-valid-minimal/`, `CIP-empty-authors/`, …) that would falsely trip that check. The runner copies each fixture into a temporary `CIP-NNNN/` directory (number taken from the fixture's frontmatter, `9999` for unassigned `?`) before invoking the validator. Expected outcome is inferred from the parent directory:

- under `cip-valid/`   → expected `pass`
- under `cip-invalid/` → expected `fail`

## Adding a fixture

1. Pick the right category (`cip-valid/` or `cip-invalid/`).
2. Create `CIP-<short-description>/README.md`. Naming convention is `CIP-valid-<x>` for valid fixtures and `CIP-<x>` for invalid (matching the existing pattern).
3. Make exactly one structural choice the test is about; everything else should be a clean baseline so the failure mode is unambiguous.
4. `bash .github/scripts/run-tests.sh <short-description>` to verify.

## CI

`.github/workflows/test-validators.yaml` runs the suite on push to `cip-validation-test`, on PRs that touch the validator or fixtures, and on `workflow_dispatch`.
