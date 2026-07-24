from fastapi import FastAPI
from fastapi.testclient import TestClient

from tmb_ai_os.api_v28 import router


def test_v28_router_registers_system_health_endpoint() -> None:
    paths = {route.path for route in router.routes if hasattr(route, "path")}

    assert "/v28/admin/dashboard/system-health" in paths


def test_system_health_endpoint_requires_authorization() -> None:
    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    response = client.get("/v28/admin/dashboard/system-health")

    assert response.status_code in {401, 403}


def test_system_health_endpoint_uses_get_method() -> None:
    matching_routes = [
        route
        for route in router.routes
        if getattr(route, "path", None) == "/v28/admin/dashboard/system-health"
    ]

    assert len(matching_routes) == 1
    assert "GET" in matching_routes[0].methods
