from tmb_ai_os.api_v13 import router


def test_v13_router_exposes_database_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v13/database/migration-status" in paths
    assert "/v13/database/config" in paths
