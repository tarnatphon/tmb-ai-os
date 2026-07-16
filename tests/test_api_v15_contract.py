from tmb_ai_os.api_v15 import router


def test_v15_router_exposes_maintenance_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v15/maintenance/preview" in paths
    assert "/v15/maintenance/run" in paths
    assert "/v15/maintenance/config" in paths
