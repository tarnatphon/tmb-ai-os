from fastapi import FastAPI

from tmb_ai_os.main import app


def test_canonical_app_exists() -> None:
    assert isinstance(app, FastAPI)


def test_canonical_app_exposes_api_routes() -> None:
    paths = set(app.openapi()["paths"])

    assert "/health" in paths
    assert "/v2/knowledge" in paths
    assert "/v3/agents" in paths
