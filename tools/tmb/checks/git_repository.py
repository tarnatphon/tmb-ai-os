from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from ..validation import ValidationResult

GitRunner = Callable[
    [
        Path,
        tuple[str, ...],
    ],
    subprocess.CompletedProcess[str],
]


def run_git(
    root: Path,
    arguments: tuple[str, ...],
) -> subprocess.CompletedProcess[str]:
    """Run a Git command without raising on a non-zero exit code."""

    return subprocess.run(
        ("git", *arguments),
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


@dataclass(frozen=True, slots=True)
class GitRepositoryCheck:
    """Check Git repository metadata and working-tree accessibility."""

    root: Path
    require_clean: bool = False
    runner: GitRunner = field(
        default=run_git,
        repr=False,
        compare=False,
    )

    def run(self) -> ValidationResult:
        """Validate the Git repository, branch, origin, and status."""

        repository = self.runner(
            self.root,
            ("rev-parse", "--show-toplevel"),
        )
        if repository.returncode != 0:
            return ValidationResult(
                name="git-repository",
                passed=False,
                message="Current directory is not a Git repository.",
            )

        errors: list[str] = []

        branch = self.runner(self.root, ("branch", "--show-current"))
        branch_name = branch.stdout.strip()
        if branch.returncode != 0 or not branch_name:
            errors.append("Unable to determine current Git branch")

        origin = self.runner(self.root, ("remote", "get-url", "origin"))
        if origin.returncode != 0 or not origin.stdout.strip():
            errors.append("Git origin remote is not configured")

        status = self.runner(self.root, ("status", "--porcelain"))
        if status.returncode != 0:
            errors.append("Unable to read Git working-tree status")
        elif self.require_clean and status.stdout.strip():
            errors.append("Git working tree is not clean")

        if errors:
            return ValidationResult(
                name="git-repository",
                passed=False,
                message="; ".join(errors),
            )

        state = "clean" if not status.stdout.strip() else "has changes"
        return ValidationResult(
            name="git-repository",
            passed=True,
            message=(f"Git repository is ready on branch {branch_name}; working tree {state}."),
            severity="info",
        )
