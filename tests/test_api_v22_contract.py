from tmb_ai_os.api_v22 import router


def test_v22_router_exposes_scope_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v22/scopes" in paths
    assert "/v22/api-keys/{key_id}/scopes" in paths
