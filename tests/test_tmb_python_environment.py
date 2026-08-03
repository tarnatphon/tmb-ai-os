from pathlib import Path

import pytest

from tools.tmb.checks.python_environment import PythonEnvironmentCheck


def write_pyproject(root: Path, requirement: str = ">=3.11") -> None:
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "test-project"\nversion = "0.0.0"\nrequires-python = "{requirement}"\n',
        encoding="utf-8",
    )


def modules_available(name: str) -> object:
    del name
    return object()


def test_python_environment_check_passes(tmp_path: Path) -> None:
    write_pyproject(tmp_path)
    check = PythonEnvironmentCheck(
        root=tmp_path,
        python_version="3.14.4",
        prefix="/tmp/venv",
        base_prefix="/usr/local",
        module_finder=modules_available,
    )

    result = check.run()

    assert result.passed is True
    assert result.severity == "info"
    assert result.message == "Python 3.14.4 environment is ready."


def test_python_environment_check_requires_pyproject(tmp_path: Path) -> None:
    check = PythonEnvironmentCheck(
        root=tmp_path,
        python_version="3.14.4",
        prefix="/tmp/venv",
        base_prefix="/usr/local",
        module_finder=modules_available,
    )

    result = check.run()

    assert result.passed is False
    assert "Missing pyproject.toml" in result.message


def test_python_environment_check_rejects_unsupported_version(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path, ">=3.14")
    check = PythonEnvironmentCheck(
        root=tmp_path,
        python_version="3.13.9",
        prefix="/tmp/venv",
        base_prefix="/usr/local",
        module_finder=modules_available,
    )

    result = check.run()

    assert result.passed is False
    assert "does not satisfy >=3.14" in result.message


def test_python_environment_check_requires_virtual_environment(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path)
    check = PythonEnvironmentCheck(
        root=tmp_path,
        python_version="3.14.4",
        prefix="/usr/local",
        base_prefix="/usr/local",
        module_finder=modules_available,
    )

    result = check.run()

    assert result.passed is False
    assert "virtual environment is not active" in result.message


def test_python_environment_check_detects_missing_modules(
    tmp_path: Path,
) -> None:
    write_pyproject(tmp_path)
    check = PythonEnvironmentCheck(
        root=tmp_path,
        python_version="3.14.4",
        prefix="/tmp/venv",
        base_prefix="/usr/local",
        module_finder=lambda name: None if name == "mypy" else object(),
    )

    result = check.run()

    assert result.passed is False
    assert "Missing development modules: mypy" in result.message


def test_python_environment_check_allows_ci_managed_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    write_pyproject(tmp_path)
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    check = PythonEnvironmentCheck(
        root=tmp_path,
        python_version="3.12.13",
        prefix="/opt/hostedtoolcache/Python/3.12.13/x64",
        base_prefix="/opt/hostedtoolcache/Python/3.12.13/x64",
        module_finder=modules_available,
    )

    result = check.run()

    assert result.passed is True
    assert result.message == "Python 3.12.13 environment is ready."
