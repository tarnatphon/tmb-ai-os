from tmb_ai_os.api_v23 import router


def test_v23_router_exposes_policy_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v23/security/policies" in paths
    assert "/v23/security/check" in paths
