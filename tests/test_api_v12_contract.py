from tmb_ai_os.api_v12 import router


def test_v12_router_exposes_deployment_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v12/deployment/status" in paths
    assert "/v12/deployment/config" in paths
