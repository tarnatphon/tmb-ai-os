from fastapi.testclient import TestClient

from tmb_ai_os.health import public_health_report
from tmb_ai_os.main import app


def test_public_health_report_contains_safe_metadata() -> None:
    report = public_health_report(
        service="tmb-ai-os",
        version="0.4.0",
    )

    assert report == {
        "status": "ok",
        "service": "tmb-ai-os",
        "version": "0.4.0",
    }


def test_public_health_endpoint() -> None:
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "tmb-ai-os",
        "version": "0.4.0",
    }
