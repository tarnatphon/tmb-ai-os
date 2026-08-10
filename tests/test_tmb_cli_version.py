import json
import subprocess
from pathlib import Path

import pytest

import tools.tmb.commands.version as version_command
from tools.tmb import main
from tools.tmb.commands.version import (
    VersionInfo,
    VersionService,
    build_json_payload,
    format_report,
)


class FakeGitRunner:
    def __init__(
        self,
        returncode: int = 0,
        stdout: str = "v0.7.1\nv0.1.0\n",
    ) -> None:
        self.returncode = returncode
        self.stdout = stdout

    def __call__(
        self,
        root: Path,
        arguments: tuple[str, ...],
    ) -> subprocess.CompletedProcess[str]:
        del root
        return subprocess.CompletedProcess(
            args=("git", *arguments),
            returncode=self.returncode,
            stdout=self.stdout,
            stderr="",
        )


def write_version_sources(root: Path, version: str) -> None:
    (root / "src" / "tmb_ai_os").mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        f'[project]\nname = "test"\nversion = "{version}"\n',
        encoding="utf-8",
    )
    (root / "src" / "tmb_ai_os" / "__init__.py").write_text(
        f'__version__ = "{version}"\n',
        encoding="utf-8",
    )


def test_version_info_reports_synchronized_versions() -> None:
    info = VersionInfo(
        package_version="0.7.1",
        module_version="0.7.1",
        latest_tag="v0.7.1",
    )

    assert info.synchronized is True


def test_version_info_detects_version_mismatch() -> None:
    info = VersionInfo(
        package_version="0.1.0",
        module_version="0.1.0",
        latest_tag="v0.7.1",
    )

    assert info.synchronized is False


def test_version_service_collects_all_sources(tmp_path: Path) -> None:
    write_version_sources(tmp_path, "0.7.1")
    service = VersionService(
        root=tmp_path,
        git_runner=FakeGitRunner(),
    )

    info = service.collect()

    assert info.package_version == "0.7.1"
    assert info.module_version == "0.7.1"
    assert info.latest_tag == "v0.7.1"
    assert info.synchronized is True


def test_format_report_shows_out_of_sync_status() -> None:
    info = VersionInfo(
        package_version="0.1.0",
        module_version="0.1.0",
        latest_tag="v0.7.1",
    )

    report = format_report(info)

    assert "Package Version : 0.1.0" in report
    assert "Latest Git Tag  : v0.7.1" in report
    assert "Status          : OUT OF SYNC" in report


def test_version_command_dispatches(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        version_command.VersionService,
        "collect",
        lambda self: VersionInfo(
            package_version="0.7.1",
            module_version="0.7.1",
            latest_tag="v0.7.1",
        ),
    )

    assert main(["version"]) == 0
    assert "Status          : OK" in capsys.readouterr().out


def test_build_json_payload_uses_stable_envelope() -> None:
    payload = build_json_payload(
        VersionInfo(
            package_version="0.1.0",
            module_version="0.1.0",
            latest_tag="v0.7.1",
        )
    )

    assert payload == {
        "schema_version": 1,
        "command": "version",
        "status": "ok",
        "data": {
            "package_version": "0.1.0",
            "module_version": "0.1.0",
            "latest_git_tag": "v0.7.1",
            "synchronized": False,
        },
    }


def test_version_json_command_outputs_json_only(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        version_command.VersionService,
        "collect",
        lambda self: VersionInfo(
            package_version="0.1.0",
            module_version="0.1.0",
            latest_tag="v0.7.1",
        ),
    )

    assert main(["version", "--json"]) == 0

    output = capsys.readouterr().out
    payload = json.loads(output)

    assert payload["schema_version"] == 1
    assert payload["command"] == "version"
    assert payload["status"] == "ok"
    assert payload["data"] == {
        "package_version": "0.1.0",
        "module_version": "0.1.0",
        "latest_git_tag": "v0.7.1",
        "synchronized": False,
    }

    assert "TMB Version" not in output
    assert "OUT OF SYNC" not in output
