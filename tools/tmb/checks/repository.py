from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..validation import ValidationResult

REQUIRED_DIRECTORIES = (
    "docs",
    "scripts",
    "src",
    "templates",
    "tests",
    "tools",
)

REQUIRED_FILES = (
    ".gitignore",
    "LICENSE",
    "README.md",
    "pyproject.toml",
)


@dataclass(frozen=True, slots=True)
class RepositoryStructureCheck:
    """Check that required repository paths exist."""

    root: Path

    def run(self) -> ValidationResult:
        """Validate required directories and files."""

        missing_paths = [
            relative_path
            for relative_path in (*REQUIRED_DIRECTORIES, *REQUIRED_FILES)
            if not (self.root / relative_path).exists()
        ]

        if missing_paths:
            missing = ", ".join(sorted(missing_paths))
            return ValidationResult(
                name="repository-structure",
                passed=False,
                message=f"Missing repository paths: {missing}",
            )

        return ValidationResult(
            name="repository-structure",
            passed=True,
            message="Required repository paths are present.",
            severity="info",
        )
