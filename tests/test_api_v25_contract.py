from tmb_ai_os.api_v25 import router


def test_v25_router_exposes_lifecycle_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v25/security/api-key-lifecycle" in paths
    assert "/v25/security/api-key-lifecycle/{api_key_id}/revoke" in paths
    assert "/v25/security/api-key-lifecycle/expiring" in paths
