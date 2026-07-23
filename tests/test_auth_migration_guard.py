from pathlib import Path


def test_dashboard_authentication_dependencies() -> None:
    api_v18 = Path("src/tmb_ai_os/api_v18.py").read_text(encoding="utf-8")
    api_v19 = Path("src/tmb_ai_os/api_v19.py").read_text(encoding="utf-8")

    assert "unified_permission_dependency" in api_v18
    assert "Permission.OPERATIONS_READ" in api_v18
    assert "scope_dependency" not in api_v18

    assert "unified_permission_dependency" in api_v19
    assert "Permission.SECURITY_ADMIN" in api_v19
    assert "scope_dependency" not in api_v19


def test_alert_dashboard_uses_unified_authentication() -> None:
    from pathlib import Path

    api_v27 = Path("src/tmb_ai_os/api_v27.py").read_text(encoding="utf-8")

    assert "unified_permission_dependency" in api_v27
    assert "Permission.SECURITY_ADMIN" in api_v27
