from pathlib import Path

from tmb_ai_os.startup_diagnostics import (
    build_startup_diagnostics,
    check_directory,
    startup_diagnostics_dict,
)


def test_directory_check_passes_for_existing_directory(
    tmp_path: Path,
) -> None:
    result = check_directory(
        name="content_directory",
        path=tmp_path,
    )

    assert result.healthy is True
    assert result.name == "content_directory"


def test_directory_check_fails_for_missing_directory(
    tmp_path: Path,
) -> None:
    missing_path = tmp_path / "missing"

    result = check_directory(
        name="content_directory",
        path=missing_path,
    )

    assert result.healthy is False
    assert "does not exist" in result.detail


def test_directory_check_can_create_output_directory(
    tmp_path: Path,
) -> None:
    output_path = tmp_path / "generated-output"

    result = check_directory(
        name="output_directory",
        path=output_path,
        create_if_missing=True,
    )

    assert result.healthy is True
    assert output_path.is_dir()


def test_startup_diagnostics_is_ready(
    tmp_path: Path,
) -> None:
    content_path = tmp_path / "content"
    output_path = tmp_path / "output"
    content_path.mkdir()

    report = build_startup_diagnostics(
        service="tmb-ai-os",
        version="0.4.0",
        content_directory=content_path,
        output_directory=output_path,
    )

    assert report.ready is True
    assert len(report.checks) == 2
    assert all(check.healthy for check in report.checks)


def test_startup_diagnostics_is_not_ready_when_content_is_missing(
    tmp_path: Path,
) -> None:
    report = build_startup_diagnostics(
        service="tmb-ai-os",
        version="0.4.0",
        content_directory=tmp_path / "missing-content",
        output_directory=tmp_path / "output",
    )

    assert report.ready is False


def test_startup_diagnostics_is_serializable(
    tmp_path: Path,
) -> None:
    content_path = tmp_path / "content"
    content_path.mkdir()

    report = build_startup_diagnostics(
        service="tmb-ai-os",
        version="0.4.0",
        content_directory=content_path,
        output_directory=tmp_path / "output",
    )

    payload = startup_diagnostics_dict(report)

    assert payload["service"] == "tmb-ai-os"
    assert payload["version"] == "0.4.0"
    assert payload["ready"] is True
