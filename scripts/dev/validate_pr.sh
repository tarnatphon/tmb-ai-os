#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo "TMB AI OS PR VALIDATION"
echo "========================================"

echo
echo "[1] Ruff"
ruff check src tests

echo
echo "[2] Mypy (PR files)"
mypy src/tmb_ai_os/core/container.py
mypy tests/test_container.py

echo
echo "[3] Pytest"
pytest -q tests/test_container.py

echo
echo "[4] Compile"
python -m compileall src

echo
echo "[5] Git Status"
git status --short

echo
echo "========================================"
echo "VALIDATION PASSED"
echo "========================================"
