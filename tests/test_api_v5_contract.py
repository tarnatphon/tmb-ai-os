from tmb_ai_os.api_v5 import router


def test_v5_router_exposes_workflow_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v5/content/preview" in paths
    assert "/v5/content/generate" in paths
    assert "/v5/content/{content_id}/status" in paths
