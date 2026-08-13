from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from ..check_registry import create_default_checks
from ..output import build_envelope, emit_json
from ..validation import ValidationSummary, run_checks

ROOT = Path(__file__).resolve().parents[3]


def register(subparsers: Any) -> None:
    """Register the repository validation command."""

    parser = subparsers.add_parser(
        "validate",
        help="Validate the TMB AI OS repository.",
        description="Validate the TMB AI OS repository.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit machine-readable JSON output.",
    )
    parser.set_defaults(handler=run)


def build_json_payload(summary: ValidationSummary) -> dict[str, Any]:
    """Build the machine-readable repository validation response."""

    return build_envelope(
        command="validate",
        status="ok" if summary.passed else "failed",
        data={
            "passed": summary.passed,
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
    """Run repository validation checks."""

    summary = run_checks(create_default_checks(ROOT))

    if getattr(args, "json_output", False):
        emit_json(build_json_payload(summary))
        return 0 if summary.passed else 1

    if summary.passed:
        print("Repository validation PASSED")
        return 0

    print("Repository validation FAILED")
    for result in summary.results:
        if not result.passed:
            print(f"- {result.name}: {result.message}")

    return 1
