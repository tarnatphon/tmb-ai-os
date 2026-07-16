from tmb_ai_os.api_v11 import router


def test_v11_router_exposes_hardening_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v11/security/config" in paths
    assert "/v11/security/rate-limit" in paths
