from __future__ import annotations

import importlib.util
import platform
import sys
import tomllib
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import InvalidVersion, Version

from ..validation import ValidationResult

REQUIRED_DEVELOPMENT_MODULES = (
    "mypy",
    "pytest",
    "ruff",
)

ModuleFinder = Callable[[str], Any | None]


@dataclass(frozen=True, slots=True)
class PythonEnvironmentCheck:
    """Check the active Python development environment."""

    root: Path
    python_version: str = field(default_factory=platform.python_version)
    prefix: str = field(default_factory=lambda: sys.prefix)
    base_prefix: str = field(default_factory=lambda: sys.base_prefix)
    module_finder: ModuleFinder = field(
        default=importlib.util.find_spec,
        repr=False,
        compare=False,
    )

    def run(self) -> ValidationResult:
        """Validate Python version, virtual environment, and tooling."""

        errors: list[str] = []
        pyproject_path = self.root / "pyproject.toml"

        if not pyproject_path.is_file():
            errors.append("Missing pyproject.toml")
        else:
            errors.extend(self._validate_python_requirement(pyproject_path))

        if self.prefix == self.base_prefix:
            errors.append("Python virtual environment is not active")

        missing_modules = [
            name for name in REQUIRED_DEVELOPMENT_MODULES if self.module_finder(name) is None
        ]
        if missing_modules:
            errors.append("Missing development modules: " + ", ".join(sorted(missing_modules)))

        if errors:
            return ValidationResult(
                name="python-environment",
                passed=False,
                message="; ".join(errors),
            )

        return ValidationResult(
            name="python-environment",
            passed=True,
            message=(f"Python {self.python_version} environment is ready."),
            severity="info",
        )

    def _validate_python_requirement(self, path: Path) -> list[str]:
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
            requirement = data["project"]["requires-python"]
        except (OSError, KeyError, TypeError, tomllib.TOMLDecodeError):
            return ["Invalid or missing project.requires-python"]

        if not isinstance(requirement, str) or not requirement.strip():
            return ["Invalid or missing project.requires-python"]

        try:
            supported = Version(self.python_version) in SpecifierSet(requirement)
        except (InvalidSpecifier, InvalidVersion):
            return ["Invalid project.requires-python specification"]

        if supported:
            return []

        return [f"Python {self.python_version} does not satisfy {requirement}"]
