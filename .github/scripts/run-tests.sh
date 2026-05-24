#!/usr/bin/env bash
# Runs validate-cip.py against every fixture under .github/tests/.
#
# Fixtures under cip-valid/   are expected to PASS validation (exit 0).
# Fixtures under cip-invalid/ are expected to FAIL validation (exit non-zero).
#
# The validator enforces directory-name == "CIP-NNNN" (zero-padded). Test
# fixtures live in descriptively-named directories (CIP-valid-minimal/ etc.),
# so each fixture is copied into a temporary CIP-NNNN/ directory before being
# validated. This isolates the directory-name check from the structural
# checks the fixtures are actually meant to exercise.
#
# Companion folders: a fixture directory may contain additional empty
# subdirectories named like 'CPS-0001/' or 'CIP-0030/'. These are copied
# alongside the temporary CIP-NNNN/ so the validator's Solution To and body
# cross-reference checks (which look up sibling folders at the repo root) can
# be exercised with controlled presence/absence of the referenced documents.
# Companion folders are tracked in git via a '.gitkeep' file inside each.
#
# Usage:
#   bash .github/scripts/run-tests.sh                 # every fixture
#   bash .github/scripts/run-tests.sh minimal         # path-substring filter
#   bash .github/scripts/run-tests.sh cip-invalid     # only the failing set
#
# Exit status: 0 if every fixture's actual outcome matched its expectation,
# 1 otherwise.

set -uo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VALIDATOR="$ROOT/.github/scripts/validate-cip.py"
TESTS_DIR="$ROOT/.github/tests"
PATTERN="${1:-}"

TMPROOT="$(mktemp -d -t cip-tests.XXXXXX)"
trap 'rm -rf "$TMPROOT"' EXIT

pass=0
fail=0

# Derive the CIP-NNNN directory name from the fixture's frontmatter.
# - "?" / "??" / etc.  -> "CIP-9999" (validator skips the dir check anyway)
# - positive integer   -> "CIP-NNNN" zero-padded to 4 digits
# - anything else      -> pass through; validator will report its own error
cip_dir_name() {
  local readme="$1"
  local raw
  # Normalize CR/CRLF -> LF so the CIP number can be extracted from
  # fixtures that deliberately use non-LF endings (those fixtures still
  # exercise the validator's line-ending check from the original file).
  raw=$(tr '\r' '\n' < "$readme" | awk '/^---/{c++; next} c==1 && /^CIP:[[:space:]]/{print $2; exit}')
  if [ -z "$raw" ] || [[ "$raw" == \?* ]]; then
    echo "CIP-9999"
  elif [[ "$raw" =~ ^[0-9]+$ ]]; then
    printf "CIP-%04d\n" "$raw"
  else
    echo "CIP-$raw"
  fi
}

run_one() {
  local readme="$1" expected="$2"
  local name="${readme#$TESTS_DIR/}"
  name="${name%/README.md}"

  if [ -n "$PATTERN" ] && [[ "$readme" != *"$PATTERN"* ]]; then
    return
  fi

  local dirname fixture_root fixture_dir fixture_src companion stderr rc actual
  dirname="$(cip_dir_name "$readme")"
  # Per-fixture root so companion folders never leak between fixtures.
  fixture_root="$(mktemp -d -p "$TMPROOT" fixture.XXXXXX)"
  fixture_dir="$fixture_root/$dirname"
  mkdir -p "$fixture_dir"
  cp "$readme" "$fixture_dir/README.md"

  # Copy any companion subdirectories (e.g. CPS-0001/) into the fixture root
  # so that validate_solution_to / validate_cross_references can find them.
  fixture_src="$(dirname "$readme")"
  for companion in "$fixture_src"/*/; do
    [ -d "$companion" ] || continue
    # Strip trailing slash so macOS cp copies the directory itself, not its
    # contents.
    cp -R "${companion%/}" "$fixture_root/"
  done

  stderr="$(python3 "$VALIDATOR" "$fixture_dir/README.md" 2>&1 1>/dev/null)"
  rc=$?
  actual="pass"; [ $rc -ne 0 ] && actual="fail"

  if [ "$actual" = "$expected" ]; then
    pass=$((pass+1))
    echo "PASS  $name"
  else
    fail=$((fail+1))
    echo "FAIL  $name  (expected=$expected, got=$actual)"
    echo "$stderr" | sed 's/^/    /'
  fi
}

while IFS= read -r -d '' readme; do
  run_one "$readme" "pass"
done < <(find "$TESTS_DIR/cip-valid" -name README.md -print0 2>/dev/null | sort -z)

while IFS= read -r -d '' readme; do
  run_one "$readme" "fail"
done < <(find "$TESTS_DIR/cip-invalid" -name README.md -print0 2>/dev/null | sort -z)

echo "---"
echo "Passed: $pass  Failed: $fail"
[ $fail -eq 0 ] || exit 1
