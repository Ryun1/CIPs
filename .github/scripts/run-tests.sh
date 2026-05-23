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
  raw=$(awk '/^---/{c++; next} c==1 && /^CIP:[[:space:]]/{print $2; exit}' "$readme")
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

  local dirname fixture_dir stderr rc actual
  dirname="$(cip_dir_name "$readme")"
  fixture_dir="$TMPROOT/$dirname"
  mkdir -p "$fixture_dir"
  cp "$readme" "$fixture_dir/README.md"

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
