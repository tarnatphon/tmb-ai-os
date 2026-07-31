#!/usr/bin/env bash
set -e

echo "========================================"
echo "TMB AI OS Environment Check"
echo "========================================"

echo "Python : $(python --version)"
echo "Ruff   : $(ruff --version)"
echo "Mypy   : $(mypy --version)"
echo "Pytest : $(pytest --version)"

echo ""
echo "Git Branch:"
git branch --show-current

echo ""
echo "Git Status:"
git status --short

echo ""
echo "Environment OK"
