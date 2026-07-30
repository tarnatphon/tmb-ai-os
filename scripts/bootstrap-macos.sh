#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")/.."

command -v python3 >/dev/null 2>&1 || {
  echo "ERROR: python3 is required. Install it with Homebrew: brew install python"
  exit 1
}

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
cp -n .env.example .env || true

./scripts/validate.sh

echo
echo "Foundation installed successfully."
echo "Run: source .venv/bin/activate"
echo "Then: uvicorn tmb_ai_os.main:app --reload"
