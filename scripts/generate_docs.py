#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

PHASE_FILES = {
    "phase0-api": [
        "docs/api/rest-api-design.md",
        "docs/api/error-handling.md",
        "docs/api/idempotency-and-retries.md",
        "docs/data/data-architecture.md",
        "docs/data/database-standards.md",
        "docs/data/data-classification.md",
        "docs/integrations/integration-architecture.md",
        "docs/integrations/webhook-security.md",
        "docs/events/event-contracts.md",
        "docs/adr/ADR-0006-api-first-design.md",
        "docs/adr/ADR-0007-postgresql-primary-database.md",
        "docs/adr/ADR-0008-versioned-event-contracts.md",
    ],
}


def validate_phase(phase: str) -> int:
    files = PHASE_FILES[phase]
    missing = []
    empty = []

    for filename in files:
        path = Path(filename)
        if not path.exists():
            missing.append(filename)
        elif path.stat().st_size == 0:
            empty.append(filename)

    print(f"Phase: {phase}")
    print(f"Expected files: {len(files)}")
    print(f"Missing files: {len(missing)}")
    print(f"Empty files: {len(empty)}")

    if missing:
        print("\nMissing:")
        for filename in missing:
            print(f"  - {filename}")

    if empty:
        print("\nEmpty:")
        for filename in empty:
            print(f"  - {filename}")

    if missing or empty:
        print("\nVALIDATION FAILED")
        return 1

    print("\nVALIDATION PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated TMB AI OS documentation.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--phase", choices=sorted(PHASE_FILES))
    group.add_argument("--all", action="store_true")
    args = parser.parse_args()

    phases = sorted(PHASE_FILES) if args.all else [args.phase]
    result = 0

    for phase in phases:
        result = max(result, validate_phase(phase))

    return result


if __name__ == "__main__":
    sys.exit(main())
