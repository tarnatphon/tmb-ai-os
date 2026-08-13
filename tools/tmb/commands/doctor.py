from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ..check_registry import create_default_checks
from ..output import build_envelope, emit_json
from ..validation import ValidationResult, ValidationSummary, run_checks

ROOT = Path(__file__).resolve().parents[3]


def register(subparsers: Any) -> None:
    """Register the developer environment doctor command."""

    parser = subparsers.add_parser(
        "doctor",
        help="Diagnose the TMB AI OS development environment.",
        description="Diagnose the TMB AI OS development environment.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit machine-readable JSON output.",
    )
    parser.set_defaults(handler=run)


def format_result(result: ValidationResult) -> str:
    """Format one validation result for human-readable output."""

    status = "PASS" if result.passed else "FAIL"
    return f"[{status}] {result.name}: {result.message}"


def build_json_payload(summary: ValidationSummary) -> dict[str, Any]:
    """Build the machine-readable doctor response."""

    return build_envelope(
        command="doctor",
        status="ok" if summary.passed else "failed",
        data={
            "healthy": summary.passed,
            "failed_count": summary.failed_count,
            "results": [
                {
                    "name": result.name,
                    "passed": result.passed,
                    "message": result.message,
                    "severity": result.severity,
                }
                for result in summary.results
            ],
        },
    )


def run(args: argparse.Namespace) -> int:
    """Run all default checks and print a diagnostic report."""

    summary = run_checks(create_default_checks(ROOT))

    if getattr(args, "json_output", False):
        emit_json(build_json_payload(summary))
        return 0 if summary.passed else 1

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
