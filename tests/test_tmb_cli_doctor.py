import argparse

import pytest

import tools.tmb.commands.doctor as doctor_command
from tools.tmb import main
from tools.tmb.commands.doctor import format_result
from tools.tmb.validation import ValidationResult


class FakeCheck:
    def __init__(self, result: ValidationResult) -> None:
        self.result = result

    def run(self) -> ValidationResult:
        return self.result


def passing_result(name: str = "example") -> ValidationResult:
    return ValidationResult(
        name=name,
        passed=True,
        message="Check passed.",
        severity="info",
    )


def failing_result(name: str = "example") -> ValidationResult:
    return ValidationResult(
        name=name,
        passed=False,
        message="Check failed.",
    )


def test_doctor_appears_in_help() -> None:
    with pytest.raises(SystemExit) as exc_info:
        main(["doctor", "--help"])

    assert exc_info.value.code == 0


def test_format_result_formats_passing_check() -> None:
    assert format_result(passing_result()) == ("[PASS] example: Check passed.")


def test_format_result_formats_failing_check() -> None:
    assert format_result(failing_result()) == ("[FAIL] example: Check failed.")


def test_doctor_returns_success_for_healthy_environment(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        doctor_command,
        "create_default_checks",
        lambda root: (FakeCheck(passing_result("repository")),),
    )

    assert doctor_command.run(argparse.Namespace()) == 0

    output = capsys.readouterr().out
    assert "[PASS] repository: Check passed." in output
    assert "Overall: HEALTHY" in output


def test_doctor_returns_failure_for_unhealthy_environment(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        doctor_command,
        "create_default_checks",
        lambda root: (
            FakeCheck(passing_result("repository")),
            FakeCheck(failing_result("toolchain")),
        ),
    )

    assert doctor_command.run(argparse.Namespace()) == 1

    output = capsys.readouterr().out
    assert "[FAIL] toolchain: Check failed." in output
    assert "Overall: UNHEALTHY (1 failed)" in output
