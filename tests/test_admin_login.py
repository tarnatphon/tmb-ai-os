from tmb_ai_os.admin_dashboard import (
    admin_dashboard,
    admin_login,
)


def test_admin_login_returns_html() -> None:
    html = admin_login()

    assert "TMB AI OS Admin" in html
    assert "/v19/admin/session" in html


def test_admin_dashboard_uses_api_key() -> None:
    html = admin_dashboard()

    assert "tmb_admin_api_key" in html
    assert "X-API-Key" in html
