from tmb_ai_os.api_v24 import router


def test_v24_router_exposes_authorization_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v24/security/authorization-events" in paths
    assert "/v24/security/policy-compliance" in paths
