from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ..check_registry import create_default_checks
from ..validation import ValidationResult, run_checks

ROOT = Path(__file__).resolve().parents[3]


def register(subparsers: Any) -> None:
    """Register the developer environment doctor command."""

    parser = subparsers.add_parser(
        "doctor",
        help="Diagnose the TMB AI OS development environment.",
        description="Diagnose the TMB AI OS development environment.",
    )
    parser.set_defaults(handler=run)


def format_result(result: ValidationResult) -> str:
    """Format one validation result for human-readable output."""

    status = "PASS" if result.passed else "FAIL"
    return f"[{status}] {result.name}: {result.message}"


def run(args: argparse.Namespace) -> int:
    """Run all default checks and print a diagnostic report."""

    del args
    summary = run_checks(create_default_checks(ROOT))

    print("TMB Doctor")
    print("=" * 60)

    for result in summary.results:
        print(format_result(result))

    print("=" * 60)

    if summary.passed:
        print("Overall: HEALTHY")
        return 0

    print(f"Overall: UNHEALTHY ({summary.failed_count} failed)")
    return 1
