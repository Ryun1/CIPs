#!/usr/bin/env bash
# Install the Python dependencies needed by validate-cip.py / validate-cps.py
# and the test runner. Use for local development; in CI the workflow installs
# these directly.
#
# Usage:
#   bash .github/scripts/setup-test-env.sh

set -euo pipefail

python3 -m pip install --upgrade pip
python3 -m pip install pyyaml jsonschema

echo
echo "Dependencies installed. Run the test suite with:"
echo "  bash .github/scripts/run-tests.sh"
