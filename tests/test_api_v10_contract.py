from tmb_ai_os.api_v10 import router


def test_v10_router_exposes_security_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v10/security/me" in paths
    assert "/v10/security/roles" in paths
    assert "/v10/security/audit" in paths
