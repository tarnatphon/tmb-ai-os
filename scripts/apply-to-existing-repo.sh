#!/usr/bin/env bash
set -Eeuo pipefail

SOURCE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="${1:-}"

if [[ -z "$TARGET_DIR" ]]; then
  echo "Usage: $0 /absolute/path/to/tmb-ai-os"
  exit 2
fi

if [[ ! -d "$TARGET_DIR/.git" ]]; then
  echo "ERROR: Target is not a Git repository: $TARGET_DIR"
  exit 1
fi

cd "$TARGET_DIR"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "ERROR: Git working tree is not clean. Commit or stash changes first."
  exit 1
fi

BRANCH="feat/sprint-1a-enterprise-foundation"
git switch -c "$BRANCH"

rsync -av --ignore-existing \
  --exclude '.git' \
  --exclude '.venv' \
  "$SOURCE_DIR/" "$TARGET_DIR/"

echo
echo "Files copied without overwriting existing files."
echo "Review: git status --short"
echo "Then run: ./scripts/bootstrap-macos.sh"
