from tmb_ai_os.api_v16 import router


def test_v16_router_exposes_alert_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v16/alerts/evaluate" in paths
    assert "/v16/incidents" in paths
    assert "/v16/incidents/{incident_id}/acknowledge" in paths
    assert "/v16/incidents/{incident_id}/resolve" in paths
