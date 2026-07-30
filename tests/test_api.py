from pathlib import Path

from fastapi.testclient import TestClient

from tmb_ai_os.main import app


def test_health_and_plugins(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.chdir(Path(__file__).parents[1])
    with TestClient(app) as client:
        health = client.get("/api/v1/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"

        plugins = client.get("/api/v1/plugins")
        assert plugins.status_code == 200
        assert plugins.json()[0]["name"] == "example-foundation"
