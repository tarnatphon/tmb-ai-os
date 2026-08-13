from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

import tools.tmb.commands.doctor as doctor_command
import tools.tmb.commands.release as release_command
import tools.tmb.commands.validate as validate_command
from tools.tmb import main
from tools.tmb.commands.release import ReleaseReadiness
from tools.tmb.commands.version import VersionInfo
from tools.tmb.validation import ValidationResult


class FakeCheck:
    def __init__(self, result: ValidationResult) -> None:
        self.result = result

    def run(self) -> ValidationResult:
        return self.result


def passing_result(name: str = "repository") -> ValidationResult:
    return ValidationResult(
        name=name,
        passed=True,
        message="Check passed.",
        severity="info",
    )


def failing_result(name: str = "toolchain") -> ValidationResult:
    return ValidationResult(
        name=name,
        passed=False,
        message="Check failed.",
    )


def fake_passing_checks(root: Path) -> tuple[FakeCheck, ...]:
    del root
    return (FakeCheck(passing_result()),)


def fake_failing_checks(root: Path) -> tuple[FakeCheck, ...]:
    del root
    return (
        FakeCheck(passing_result()),
        FakeCheck(failing_result()),
    )


def test_validate_json_outputs_machine_readable_summary(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(validate_command, "create_default_checks", fake_passing_checks)

    assert main(["validate", "--json"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload == {
        "schema_version": 1,
        "command": "validate",
        "status": "ok",
        "data": {
            "passed": True,
            "failed_count": 0,
            "results": [
                {
                    "name": "repository",
                    "passed": True,
                    "message": "Check passed.",
                    "severity": "info",
                },
            ],
        },
    }


def test_validate_json_returns_failure_code_for_failed_checks(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(validate_command, "create_default_checks", fake_failing_checks)

    assert main(["validate", "--json"]) == 1

    payload = json.loads(capsys.readouterr().out)
    assert payload["status"] == "failed"
    assert payload["data"]["passed"] is False
    assert payload["data"]["failed_count"] == 1


def test_doctor_json_outputs_machine_readable_summary(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(doctor_command, "create_default_checks", fake_failing_checks)

    assert main(["doctor", "--json"]) == 1

    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["schema_version"] == 1
    assert payload["command"] == "doctor"
    assert payload["status"] == "failed"
    assert payload["data"]["healthy"] is False
    assert payload["data"]["failed_count"] == 1
    assert payload["data"]["results"][1] == {
        "name": "toolchain",
        "passed": False,
        "message": "Check failed.",
        "severity": "error",
    }
    assert "TMB Doctor" not in output


def test_release_json_payload_preserves_readiness_details() -> None:
    payload = release_command.build_json_payload(
        ReleaseReadiness(
            ready=False,
            reasons=("Git working tree is not clean",),
            version_info=VersionInfo(
                package_version="0.1.0",
                module_version="0.1.0",
                latest_tag="v0.7.1",
            ),
        )
    )

    assert payload == {
        "schema_version": 1,
        "command": "release",
        "status": "failed",
        "data": {
            "ready": False,
            "reasons": ["Git working tree is not clean"],
            "version": {
                "package_version": "0.1.0",
                "module_version": "0.1.0",
                "latest_git_tag": "v0.7.1",
                "synchronized": False,
            },
        },
    }


def test_release_json_command_outputs_json_only(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        release_command.ReleaseService,
        "inspect",
        lambda self: ReleaseReadiness(
            ready=True,
            reasons=(),
            version_info=VersionInfo(
                package_version="0.7.1",
                module_version="0.7.1",
                latest_tag="v0.7.1",
            ),
        ),
    )

    assert release_command.run(argparse.Namespace(json_output=True)) == 0

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["command"] == "release"
    assert payload["status"] == "ok"
    assert payload["data"]["ready"] is True
    assert "TMB Release Readiness" not in output
