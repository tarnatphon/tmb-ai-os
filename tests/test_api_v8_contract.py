from tmb_ai_os.api_v8 import router


def test_v8_router_exposes_scheduled_publish_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v8/publish-queue/{queue_id}/schedule" in paths
    assert "/v8/publish-queue/process-due" in paths
    assert "/v8/publish-queue/failed" in paths
