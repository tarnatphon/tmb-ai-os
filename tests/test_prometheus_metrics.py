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
