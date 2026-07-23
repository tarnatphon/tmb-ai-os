from tmb_ai_os.admin_dashboard import admin_dashboard


def test_admin_dashboard_returns_html() -> None:
    html = admin_dashboard()

    assert "TMB AI OS" in html
    assert "/v18/dashboard/summary" in html


def test_admin_dashboard_loads_alert_metrics() -> None:
    html = admin_dashboard()

    assert "/v27/admin/dashboard/alerts" in html
    assert 'id="alert-summary"' in html
    assert 'id="alerts-updated"' in html


def test_admin_dashboard_displays_alert_metric_cards() -> None:
    html = admin_dashboard()

    assert "Alerts Routed" in html
    assert "Delivery Success Rate" in html
    assert "Delivery Failed" in html
    assert "Delivery Suppressed" in html
    assert "Fallback Alerts" in html
    assert "No Route" in html


def test_admin_dashboard_formats_alert_metrics() -> None:
    html = admin_dashboard()

    assert "formatPercent" in html
    assert "formatDateTime" in html
    assert "alerts.delivery.success_rate" in html
    assert "alerts.generated_at" in html
