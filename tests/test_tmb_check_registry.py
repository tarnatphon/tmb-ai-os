from pathlib import Path

from tools.tmb.check_registry import create_default_checks
from tools.tmb.checks import (
    GitRepositoryCheck,
    PythonEnvironmentCheck,
    RepositoryStructureCheck,
    ToolchainCheck,
    WorkflowStructureCheck,
)


def test_default_check_registry_preserves_execution_order(
    tmp_path: Path,
) -> None:
    checks = create_default_checks(tmp_path)

    assert [type(check) for check in checks] == [
        RepositoryStructureCheck,
        PythonEnvironmentCheck,
        GitRepositoryCheck,
        WorkflowStructureCheck,
        ToolchainCheck,
    ]
