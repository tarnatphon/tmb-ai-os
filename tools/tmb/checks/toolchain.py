from __future__ import annotations

import shutil
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

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

    executable_dir: Path | None = None
    finder: ToolFinder = field(
        default=shutil.which,
        repr=False,
        compare=False,
    )

    def run(self) -> ValidationResult:
        """Validate the required development toolchain."""

        missing_tools = sorted(tool for tool in REQUIRED_TOOLS if self._find(tool) is None)

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

    def _find(self, tool: str) -> str | None:
        found = self.finder(tool)
        if found is not None:
            return found

        if self.executable_dir is None:
            return None

        candidate = self.executable_dir / tool
        if candidate.exists():
            return str(candidate)

        return None
