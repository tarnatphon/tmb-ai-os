from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ..check_registry import create_default_checks
from ..validation import run_checks

ROOT = Path(__file__).resolve().parents[3]


def register(subparsers: Any) -> None:
    """Register the repository validation command."""

    parser = subparsers.add_parser(
        "validate",
        help="Validate the TMB AI OS repository.",
        description="Validate the TMB AI OS repository.",
    )
    parser.set_defaults(handler=run)


def run(args: argparse.Namespace) -> int:
    """Run repository validation checks."""

    del args
    summary = run_checks(create_default_checks(ROOT))

    if summary.passed:
        print("Repository validation PASSED")
        return 0

    print("Repository validation FAILED")
    for result in summary.results:
        if not result.passed:
            print(f"- {result.name}: {result.message}")

    return 1
