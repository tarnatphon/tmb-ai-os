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


def test_admin_dashboard_auto_refreshes_alert_metrics() -> None:
    html = admin_dashboard()

    assert "ALERT_REFRESH_INTERVAL_MS=10000" in html
    assert "scheduleAlertRefresh" in html
    assert "stopAlertRefresh" in html
    assert "window.setTimeout" in html


def test_admin_dashboard_pauses_refresh_for_hidden_tabs() -> None:
    html = admin_dashboard()

    assert 'document.addEventListener("visibilitychange"' in html
    assert "document.hidden" in html
    assert 'setAlertStatus("Paused","paused")' in html
    assert "resumeAlertRefresh" in html


def test_admin_dashboard_prevents_overlapping_alert_requests() -> None:
    html = admin_dashboard()

    assert "let alertRefreshInFlight=false" in html
    assert "if(alertRefreshInFlight){return}" in html
    assert "alertRefreshInFlight=true" in html
    assert "alertRefreshInFlight=false" in html


def test_admin_dashboard_displays_live_refresh_status() -> None:
    html = admin_dashboard()

    assert 'id="alert-live-status"' in html
    assert 'setAlertStatus("Live","live")' in html
    assert 'setAlertStatus("Refreshing","refreshing")' in html
    assert 'setAlertStatus("Error","error")' in html


def test_admin_dashboard_displays_refresh_controls() -> None:
    html = admin_dashboard()

    assert 'id="alert-refresh-toggle"' in html
    assert 'id="alert-refresh-interval"' in html
    assert 'id="alert-refresh-now"' in html
    assert 'id="alert-refresh-countdown"' in html


def test_admin_dashboard_supports_refresh_intervals() -> None:
    html = admin_dashboard()

    assert '<option value="10000">' in html
    assert '<option value="30000">' in html
    assert '<option value="60000">' in html
    assert "changeAlertRefreshInterval" in html


def test_admin_dashboard_persists_refresh_preferences() -> None:
    html = admin_dashboard()

    assert 'ALERT_REFRESH_ENABLED_KEY="tmb_alert_refresh_enabled"' in html
    assert 'ALERT_REFRESH_INTERVAL_KEY="tmb_alert_refresh_interval"' in html
    assert "localStorage.getItem(ALERT_REFRESH_ENABLED_KEY)" in html
    assert "localStorage.setItem(" in html


def test_admin_dashboard_displays_refresh_countdown() -> None:
    html = admin_dashboard()

    assert "updateAlertCountdown" in html
    assert "nextAlertRefreshAt" in html
    assert "window.setInterval" in html
    assert "รีเฟรชครั้งถัดไปใน" in html


def test_admin_dashboard_supports_manual_alert_refresh() -> None:
    html = admin_dashboard()

    assert "refreshAlertsNow" in html
    assert "Manual alert refresh failed" in html
    assert 'addEventListener("click"' in html
