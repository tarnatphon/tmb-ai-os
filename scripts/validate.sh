#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "$0")/.."

export PYTHONPATH="${PWD}/src${PYTHONPATH:+:${PYTHONPATH}}"
python -m compileall -q src tests

if command -v ruff >/dev/null 2>&1; then
  ruff check .
else
  echo "NOTICE: ruff is not installed; compile and tests will still run."
fi

if command -v mypy >/dev/null 2>&1; then
  mypy src
else
  echo "NOTICE: mypy is not installed; compile and tests will still run."
fi

pytest

echo "ALL AVAILABLE VALIDATION CHECKS PASSED"
