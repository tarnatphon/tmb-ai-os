from tmb_ai_os.api_v17 import router


def test_v17_router_exposes_notification_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v17/notifications/test" in paths
    assert "/v17/notifications/deliveries" in paths
    assert "/v17/incidents/{incident_id}/escalate" in paths
