from datetime import UTC, datetime

from fastapi.testclient import TestClient

from tmb_ai_os.alert_observability import (
    alert_observability,
    reset_alert_metrics,
)
from tmb_ai_os.alert_router import RoutingResult
from tmb_ai_os.api import app
from tmb_ai_os.http_metrics import HttpMetricsCollector
from tmb_ai_os.prometheus_metrics import render_prometheus_metrics


def test_render_empty_prometheus_metrics() -> None:
    collector = HttpMetricsCollector()

    output = render_prometheus_metrics(collector.snapshot())

    assert "# TYPE tmb_http_requests_total counter" in output
    assert "tmb_http_requests_total 0" in output
    assert "tmb_http_successful_requests_total 0" in output
    assert "tmb_http_client_errors_total 0" in output
    assert "tmb_http_server_errors_total 0" in output
    assert output.endswith("\n")


def test_render_prometheus_metrics_with_labels() -> None:
    collector = HttpMetricsCollector()
    collector.record(
        method="GET",
        status_code=200,
        duration_ms=10.5,
    )
    collector.record(
        method="POST",
        status_code=503,
        duration_ms=20.5,
    )

    output = render_prometheus_metrics(collector.snapshot())

    assert "tmb_http_requests_total 2" in output
    assert "tmb_http_successful_requests_total 1" in output
    assert "tmb_http_server_errors_total 1" in output
    assert "tmb_http_request_duration_milliseconds_total 31.0" in output
    assert 'tmb_http_requests_by_method_total{method="GET"} 1' in output
    assert 'tmb_http_requests_by_method_total{method="POST"} 1' in output
    assert 'tmb_http_requests_by_status_total{status="200"} 1' in output
    assert 'tmb_http_requests_by_status_total{status="503"} 1' in output


def test_prometheus_label_values_are_escaped() -> None:
    collector = HttpMetricsCollector()
    collector.record(
        method='CUSTOM"METHOD',
        status_code=200,
        duration_ms=1.0,
    )

    output = render_prometheus_metrics(collector.snapshot())

    assert 'method="CUSTOM\\"METHOD"' in output


def test_render_prometheus_alert_metrics() -> None:
    from tmb_ai_os.alert_observability import AlertMetricsSnapshot

    collector = HttpMetricsCollector()
    alert_snapshot = AlertMetricsSnapshot(
        routed_total=8,
        delivery_success_total=5,
        delivery_failed_total=2,
        delivery_suppressed_total=1,
        fallback_total=2,
        no_route_total=1,
    )

    output = render_prometheus_metrics(
        collector.snapshot(),
        alert_snapshot,
    )

    assert "# TYPE tmb_alerts_routed_total counter" in output
    assert "tmb_alerts_routed_total 8" in output
    assert "tmb_alert_delivery_success_total 5" in output
    assert "tmb_alert_delivery_failed_total 2" in output
    assert "tmb_alert_delivery_suppressed_total 1" in output
    assert "tmb_alert_fallback_total 2" in output
    assert "tmb_alert_no_route_total 1" in output


def test_alert_metrics_are_optional() -> None:
    collector = HttpMetricsCollector()

    output = render_prometheus_metrics(collector.snapshot())

    assert "tmb_alerts_routed_total" not in output


def test_prometheus_api_includes_alert_metrics() -> None:
    from tmb_ai_os.alert_observability import (
        alert_observability,
        reset_alert_metrics,
    )
    from tmb_ai_os.api_v9 import prometheus_metrics

    reset_alert_metrics()

    response = prometheus_metrics()
    body = response.body.decode()

    assert response.status_code == 200
    assert "tmb_alerts_routed_total 0" in body
    assert "tmb_alert_delivery_success_total 0" in body
    assert "tmb_alert_delivery_failed_total 0" in body
    assert "tmb_alert_delivery_suppressed_total 0" in body
    assert "tmb_alert_fallback_total 0" in body
    assert "tmb_alert_no_route_total 0" in body

    alert_observability.reset()


def test_prometheus_endpoint_exports_shared_alert_metrics() -> None:
    reset_alert_metrics()

    try:
        result = RoutingResult(
            alert_id="integration-alert",
            channels=("webhook",),
            deliveries=(),
            routed_at=datetime.now(UTC),
        )
        alert_observability.record(result)

        with TestClient(app) as client:
            response = client.get("/v9/metrics/prometheus")

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain; version=0.0.4")
        assert "tmb_alerts_routed_total 1" in response.text
    finally:
        reset_alert_metrics()
