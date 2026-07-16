from tmb_ai_os.api_v18 import router


def test_v18_router_exposes_dashboard_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v18/dashboard/summary" in paths
    assert "/v18/dashboard/incidents" in paths
    assert "/v18/dashboard/notifications" in paths
