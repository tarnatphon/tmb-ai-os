from tmb_ai_os.api_v26 import router


def test_v26_router_exposes_telemetry_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v26/security/api-key-telemetry/{api_key_id}/risk" in paths
    assert "/v26/security/api-key-telemetry/{api_key_id}/events" in paths
