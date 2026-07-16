from tmb_ai_os.admin_dashboard import admin_dashboard


def test_admin_dashboard_returns_html() -> None:
    html = admin_dashboard()

    assert "TMB AI OS" in html
    assert "/v18/dashboard/summary" in html
