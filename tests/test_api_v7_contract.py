from tmb_ai_os.api_v7 import router


def test_v7_router_exposes_publish_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v7/publishers" in paths
    assert "/v7/publish-queue/process" in paths
    assert "/v7/publish-queue/{queue_id}" in paths
