from tmb_ai_os.api_v9 import router


def test_v9_router_exposes_observability_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v9/health/live" in paths
    assert "/v9/health/ready" in paths
    assert "/v9/metrics/operations" in paths
    assert "/v9/metrics/publish-queue" in paths
    assert "/v9/metrics/content" in paths
    assert "/v9/metrics/http" in paths
    assert "/v9/metrics/prometheus" in paths
