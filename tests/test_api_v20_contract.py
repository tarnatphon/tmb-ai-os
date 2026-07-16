from tmb_ai_os.api_v20 import router


def test_v20_router_exposes_api_key_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v20/api-keys" in paths
    assert "/v20/api-keys/{key_id}/revoke" in paths
    assert "/v20/api-keys/{key_id}/rotate" in paths
