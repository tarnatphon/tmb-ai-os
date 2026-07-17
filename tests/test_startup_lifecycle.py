import os
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from tmb_ai_os.main import app
from tmb_ai_os.startup_diagnostics import StartupDiagnostics


def test_lifespan_stores_startup_diagnostics() -> None:
    expected_report = StartupDiagnostics(
        service="tmb-ai-os",
        version=app.version,
        ready=True,
        checks=(),
    )

    environment = {
        "TMB_CONTENT_DIR": "test-content",
        "TMB_OUTPUT_DIR": "test-output",
    }

    with (
        patch.dict(os.environ, environment),
        patch(
            "tmb_ai_os.lifecycle.build_startup_diagnostics",
            return_value=expected_report,
        ) as build_mock,
        patch("tmb_ai_os.lifecycle.log_startup_diagnostics") as log_mock,
        TestClient(app),
    ):
        assert app.state.startup_diagnostics == expected_report

    build_mock.assert_called_once_with(
        service="tmb-ai-os",
        version=app.version,
        content_directory=Path("test-content"),
        output_directory=Path("test-output"),
    )
    log_mock.assert_called_once_with(expected_report)


def test_application_starts_when_diagnostics_are_not_ready() -> None:
    report = StartupDiagnostics(
        service="tmb-ai-os",
        version=app.version,
        ready=False,
        checks=(),
    )

    with (
        patch(
            "tmb_ai_os.lifecycle.build_startup_diagnostics",
            return_value=report,
        ),
        patch("tmb_ai_os.lifecycle.log_startup_diagnostics"),
        TestClient(app) as client,
    ):
        response = client.get("/health")
        stored_report = app.state.startup_diagnostics

    assert response.status_code == 200
    assert stored_report == report
    assert stored_report.ready is False
