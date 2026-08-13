from __future__ import annotations

import argparse
import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from ..check_registry import create_default_checks
from ..output import build_envelope, emit_json
from ..validation import run_checks
from .version import VersionInfo, VersionService

ROOT = Path(__file__).resolve().parents[3]

GitRunner = Callable[
    [Path, tuple[str, ...]],
    subprocess.CompletedProcess[str],
]


def run_git(
    root: Path,
    arguments: tuple[str, ...],
) -> subprocess.CompletedProcess[str]:
    """Run Git without raising for a non-zero exit code."""

    return subprocess.run(
        ("git", *arguments),
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


@dataclass(frozen=True, slots=True)
class ReleaseReadiness:
    """Release-readiness result."""

    ready: bool
    reasons: tuple[str, ...]
    version_info: VersionInfo


@dataclass(frozen=True, slots=True)
class ReleaseService:
    """Evaluate whether the repository is ready for release."""

    root: Path
    git_runner: GitRunner = field(
        default=run_git,
        repr=False,
        compare=False,
    )

    def inspect(self) -> ReleaseReadiness:
        """Inspect validation, Git, and version release requirements."""

        reasons: list[str] = []
        summary = run_checks(create_default_checks(self.root))

        if not summary.passed:
            reasons.append(f"Repository validation failed ({summary.failed_count} checks)")

        branch = self.git_runner(self.root, ("branch", "--show-current"))
        if branch.returncode != 0 or branch.stdout.strip() != "main":
            reasons.append("Release must run from the main branch")

        status = self.git_runner(self.root, ("status", "--porcelain"))
        if status.returncode != 0:
            reasons.append("Unable to read Git working-tree status")
        elif status.stdout.strip():
            reasons.append("Git working tree is not clean")

        sync = self.git_runner(
            self.root,
            ("rev-list", "--left-right", "--count", "HEAD...origin/main"),
        )
        if sync.returncode != 0:
            reasons.append("Unable to compare HEAD with origin/main")
        elif sync.stdout.strip() != "0\t0":
            reasons.append("Local main is not synchronized with origin/main")

        version_info = VersionService(self.root).collect()
        if not version_info.synchronized:
            reasons.append("Project version sources are out of sync")

        return ReleaseReadiness(
            ready=not reasons,
            reasons=tuple(reasons),
            version_info=version_info,
        )


def register(subparsers: Any) -> None:
    """Register the release-readiness command."""

    parser = subparsers.add_parser(
        "release",
        help="Check whether TMB AI OS is ready for release.",
        description="Check whether TMB AI OS is ready for release.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Emit machine-readable JSON output.",
    )
    parser.set_defaults(handler=run)


def format_report(readiness: ReleaseReadiness) -> str:
    """Format release-readiness information."""

    status = "READY" if readiness.ready else "NOT READY"
    lines = [
        "TMB Release Readiness",
        "=" * 60,
        f"Package Version : {readiness.version_info.package_version}",
        f"Module Version  : {readiness.version_info.module_version}",
        f"Latest Git Tag  : {readiness.version_info.latest_tag or 'NONE'}",
        f"Status          : {status}",
    ]

    if readiness.reasons:
        lines.append("Reasons:")
        lines.extend(f"- {reason}" for reason in readiness.reasons)

    lines.append("=" * 60)
    return "\n".join(lines)


def build_json_payload(readiness: ReleaseReadiness) -> dict[str, Any]:
    """Build the machine-readable release-readiness response."""

    return build_envelope(
        command="release",
        status="ok" if readiness.ready else "failed",
        data={
            "ready": readiness.ready,
            "reasons": list(readiness.reasons),
            "version": {
                "package_version": readiness.version_info.package_version,
                "module_version": readiness.version_info.module_version,
                "latest_git_tag": readiness.version_info.latest_tag,
                "synchronized": readiness.version_info.synchronized,
            },
        },
    )


def run(args: argparse.Namespace) -> int:
    """Display the release-readiness report."""

    try:
        readiness = ReleaseService(ROOT).inspect()
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"Release inspection FAILED: {exc}")
        return 1

    if getattr(args, "json_output", False):
        emit_json(build_json_payload(readiness))
    else:
        print(format_report(readiness))

    return 0 if readiness.ready else 1
