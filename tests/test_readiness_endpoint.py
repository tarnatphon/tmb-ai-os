from unittest.mock import patch

from fastapi.testclient import TestClient

from tmb_ai_os.health import HealthCheck, ReadinessReport
from tmb_ai_os.main import app


def test_readiness_endpoint_returns_200_when_ready() -> None:
    report = ReadinessReport(
        ready=True,
        checks=(
            HealthCheck(
                name="database",
                healthy=True,
                detail="Database connection is available",
            ),
        ),
    )

    with patch(
        "tmb_ai_os.api_v9.build_readiness_report",
        return_value=report,
    ):
        response = TestClient(app).get("/v9/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "ready": True,
        "checks": [
            {
                "name": "database",
                "healthy": True,
                "detail": "Database connection is available",
            }
        ],
    }


def test_readiness_endpoint_returns_503_when_not_ready() -> None:
    report = ReadinessReport(
        ready=False,
        checks=(
            HealthCheck(
                name="database",
                healthy=False,
                detail="Database connection failed",
            ),
        ),
    )

    with patch(
        "tmb_ai_os.api_v9.build_readiness_report",
        return_value=report,
    ):
        response = TestClient(app).get("/v9/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "ready": False,
        "checks": [
            {
                "name": "database",
                "healthy": False,
                "detail": "Database connection failed",
            }
        ],
    }
