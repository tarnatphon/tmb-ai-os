from __future__ import annotations

import sys
from pathlib import Path

from .checks import (
    GitRepositoryCheck,
    PythonEnvironmentCheck,
    RepositoryStructureCheck,
    ToolchainCheck,
    WorkflowStructureCheck,
)
from .validation import ValidationCheck


def create_default_checks(root: Path) -> tuple[ValidationCheck, ...]:
    """Create validation checks in their execution order."""

    return (
        RepositoryStructureCheck(root),
        PythonEnvironmentCheck(root),
        GitRepositoryCheck(root),
        WorkflowStructureCheck(root),
        ToolchainCheck(executable_dir=Path(sys.executable).parent),
    )
