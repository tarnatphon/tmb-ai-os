from tmb_ai_os.api_v14 import router


def test_v14_router_exposes_backup_routes() -> None:
    paths = {route.path for route in router.routes}

    assert "/v14/backups" in paths
    assert "/v14/backups/create" in paths
    assert "/v14/backups/{backup_name}/verify" in paths
