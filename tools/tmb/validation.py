from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from typing import Literal, Protocol

ValidationSeverity = Literal["info", "warning", "error"]


@dataclass(frozen=True, slots=True)
class ValidationResult:
    """Result produced by one repository validation check."""

    name: str
    passed: bool
    message: str
    severity: ValidationSeverity = "error"


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    """Aggregate result produced by the validation runner."""

    results: tuple[ValidationResult, ...]

    @property
    def passed(self) -> bool:
        """Return whether every validation check passed."""

        return all(result.passed for result in self.results)

    @property
    def failed_count(self) -> int:
        """Return the number of failed validation checks."""

        return sum(not result.passed for result in self.results)


class ValidationCheck(Protocol):
    """Contract implemented by repository validation checks."""

    def run(self) -> ValidationResult:
        """Execute the validation check."""


def run_checks(checks: Iterable[ValidationCheck]) -> ValidationSummary:
    """Execute validation checks in their configured order."""

    return ValidationSummary(
        results=tuple(check.run() for check in checks),
    )
