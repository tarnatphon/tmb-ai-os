from tmb_ai_os.api_v21 import router


def test_v21_router_exposes_auth_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v21/auth/status" in paths
    assert "/v21/auth/validate" in paths
