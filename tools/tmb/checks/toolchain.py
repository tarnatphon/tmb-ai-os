from __future__ import annotations

import shutil
from collections.abc import Callable
from dataclasses import dataclass, field

from ..validation import ValidationResult

REQUIRED_TOOLS = (
    "git",
    "mypy",
    "pytest",
    "python",
    "ruff",
)

ToolFinder = Callable[[str], str | None]


@dataclass(frozen=True, slots=True)
class ToolchainCheck:
    """Check that required development commands are available."""

    finder: ToolFinder = field(
        default=shutil.which,
        repr=False,
        compare=False,
    )

    def run(self) -> ValidationResult:
        """Validate the required development toolchain."""

        missing_tools = sorted(tool for tool in REQUIRED_TOOLS if self.finder(tool) is None)

        if missing_tools:
            return ValidationResult(
                name="toolchain",
                passed=False,
                message=("Missing development tools: " + ", ".join(missing_tools)),
            )

        return ValidationResult(
            name="toolchain",
            passed=True,
            message="Development toolchain is ready.",
            severity="info",
        )
