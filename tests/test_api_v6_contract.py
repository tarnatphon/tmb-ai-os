from tmb_ai_os.api_v6 import router


def test_v6_router_exposes_editorial_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v6/content/{content_id}/review" in paths
    assert "/v6/content/{content_id}/approve" in paths
    assert "/v6/content/{content_id}/reject" in paths
    assert "/v6/content/{content_id}/publish" in paths
    assert "/v6/publish-queue" in paths
    assert "/v6/content/{content_id}/audit" in paths
