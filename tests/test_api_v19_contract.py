from tmb_ai_os.api_v19 import router


def test_v19_router_exposes_admin_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v19/admin/session" in paths
    assert "/v19/admin/audit" in paths
