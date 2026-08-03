from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from ..validation import ValidationResult


def _read_workflow_name(path: Path) -> str | None:
    """Read a workflow name from its top-level name field."""

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None

    for line in lines:
        if not line.startswith("name:"):
            continue

        value = line.partition(":")[2].strip().strip("\"'")
        return value or None

    return None


@dataclass(frozen=True, slots=True)
class WorkflowStructureCheck:
    """Check the structure and names of GitHub Actions workflows."""

    root: Path

    def run(self) -> ValidationResult:
        """Validate workflow directory, files, and unique names."""

        workflow_directory = self.root / ".github" / "workflows"
        if not workflow_directory.is_dir():
            return ValidationResult(
                name="workflow-structure",
                passed=False,
                message="Missing .github/workflows directory.",
            )

        workflow_files = sorted(
            (
                *workflow_directory.glob("*.yml"),
                *workflow_directory.glob("*.yaml"),
            ),
            key=lambda path: path.name,
        )

        if not workflow_files:
            return ValidationResult(
                name="workflow-structure",
                passed=False,
                message="No GitHub Actions workflow files were found.",
            )

        missing_names: list[str] = []
        workflow_names: list[str] = []

        for workflow_file in workflow_files:
            workflow_name = _read_workflow_name(workflow_file)
            if workflow_name is None:
                missing_names.append(workflow_file.name)
            else:
                workflow_names.append(workflow_name)

        errors: list[str] = []

        if missing_names:
            errors.append("Workflows missing a name: " + ", ".join(sorted(missing_names)))

        duplicate_names = sorted(
            name for name, count in Counter(workflow_names).items() if count > 1
        )
        if duplicate_names:
            errors.append("Duplicate workflow names: " + ", ".join(duplicate_names))

        if errors:
            return ValidationResult(
                name="workflow-structure",
                passed=False,
                message="; ".join(errors),
            )

        return ValidationResult(
            name="workflow-structure",
            passed=True,
            message=f"Validated {len(workflow_files)} workflow files.",
            severity="info",
        )
