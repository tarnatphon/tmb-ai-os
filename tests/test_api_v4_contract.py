from tmb_ai_os.api_v4 import router


def test_v4_router_exposes_content_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v4/content" in paths
    assert "/v4/content/{content_id}" in paths
