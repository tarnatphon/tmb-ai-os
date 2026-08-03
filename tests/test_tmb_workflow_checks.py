from pathlib import Path

from tools.tmb.checks.workflow import WorkflowStructureCheck


def write_workflow(root: Path, filename: str, content: str) -> None:
    workflow_directory = root / ".github" / "workflows"
    workflow_directory.mkdir(parents=True, exist_ok=True)
    (workflow_directory / filename).write_text(content, encoding="utf-8")


def test_workflow_structure_check_passes(tmp_path: Path) -> None:
    write_workflow(tmp_path, "ci.yml", "name: CI\non: push\n")
    write_workflow(
        tmp_path,
        "quality.yaml",
        "name: Foundation Quality\non: pull_request\n",
    )

    result = WorkflowStructureCheck(tmp_path).run()

    assert result.passed is True
    assert result.severity == "info"
    assert result.message == "Validated 2 workflow files."


def test_workflow_structure_check_requires_directory(
    tmp_path: Path,
) -> None:
    result = WorkflowStructureCheck(tmp_path).run()

    assert result.passed is False
    assert "Missing .github/workflows directory" in result.message


def test_workflow_structure_check_requires_workflow_files(
    tmp_path: Path,
) -> None:
    (tmp_path / ".github" / "workflows").mkdir(parents=True)

    result = WorkflowStructureCheck(tmp_path).run()

    assert result.passed is False
    assert "No GitHub Actions workflow files" in result.message


def test_workflow_structure_check_requires_names(tmp_path: Path) -> None:
    write_workflow(tmp_path, "missing-name.yml", "on: push\n")

    result = WorkflowStructureCheck(tmp_path).run()

    assert result.passed is False
    assert "Workflows missing a name: missing-name.yml" in result.message


def test_workflow_structure_check_rejects_duplicate_names(
    tmp_path: Path,
) -> None:
    write_workflow(tmp_path, "first.yml", "name: CI\non: push\n")
    write_workflow(tmp_path, "second.yaml", "name: CI\non: pull_request\n")

    result = WorkflowStructureCheck(tmp_path).run()

    assert result.passed is False
    assert "Duplicate workflow names: CI" in result.message


def test_workflow_structure_check_accepts_quoted_name(
    tmp_path: Path,
) -> None:
    write_workflow(tmp_path, "quoted.yml", 'name: "Release Validation"\n')

    result = WorkflowStructureCheck(tmp_path).run()

    assert result.passed is True
