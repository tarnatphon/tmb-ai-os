from pathlib import Path

import pytest

import tools.tmb.commands.validate as validate_command
from tools.tmb import main
from tools.tmb.checks.repository import (
    REQUIRED_DIRECTORIES,
    REQUIRED_FILES,
    RepositoryStructureCheck,
)


def create_required_paths(root: Path) -> None:
    for relative_path in REQUIRED_DIRECTORIES:
        (root / relative_path).mkdir(parents=True, exist_ok=True)

    for relative_path in REQUIRED_FILES:
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("", encoding="utf-8")


def test_repository_structure_check_passes(tmp_path: Path) -> None:
    create_required_paths(tmp_path)

    result = RepositoryStructureCheck(tmp_path).run()

    assert result.passed is True
    assert result.severity == "info"
    assert result.message == "Required repository paths are present."


def test_repository_structure_check_detects_missing_directory(
    tmp_path: Path,
) -> None:
    create_required_paths(tmp_path)
    (tmp_path / "tools").rmdir()

    result = RepositoryStructureCheck(tmp_path).run()

    assert result.passed is False
    assert "tools" in result.message


def test_repository_structure_check_detects_missing_file(
    tmp_path: Path,
) -> None:
    create_required_paths(tmp_path)
    (tmp_path / "README.md").unlink()

    result = RepositoryStructureCheck(tmp_path).run()

    assert result.passed is False
    assert "README.md" in result.message


def test_repository_structure_check_sorts_missing_paths(
    tmp_path: Path,
) -> None:
    result = RepositoryStructureCheck(tmp_path).run()

    expected = sorted((*REQUIRED_DIRECTORIES, *REQUIRED_FILES))
    positions = [result.message.index(path) for path in expected]

    assert positions == sorted(positions)


def test_validate_command_returns_failure_for_invalid_repository(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(validate_command, "ROOT", tmp_path)

    assert main(["validate"]) == 1

    output = capsys.readouterr().out
    assert "Repository validation FAILED" in output
    assert "repository-structure" in output
