from tmb_ai_os.http_metrics import (
    HttpMetricsCollector,
    get_http_metrics,
    record_http_request,
    reset_http_metrics,
)


def test_new_collector_returns_empty_snapshot() -> None:
    collector = HttpMetricsCollector()

    snapshot = collector.snapshot()

    assert snapshot.total_requests == 0
    assert snapshot.successful_requests == 0
    assert snapshot.client_errors == 0
    assert snapshot.server_errors == 0
    assert snapshot.total_duration_ms == 0.0
    assert snapshot.average_duration_ms == 0.0
    assert snapshot.maximum_duration_ms == 0.0
    assert snapshot.requests_by_method == {}
    assert snapshot.requests_by_status == {}


def test_collector_records_requests_by_status_and_method() -> None:
    collector = HttpMetricsCollector()

    collector.record(
        method="get",
        status_code=200,
        duration_ms=10.0,
    )
    collector.record(
        method="POST",
        status_code=404,
        duration_ms=20.0,
    )
    collector.record(
        method="GET",
        status_code=503,
        duration_ms=30.0,
    )

    snapshot = collector.snapshot()

    assert snapshot.total_requests == 3
    assert snapshot.successful_requests == 1
    assert snapshot.client_errors == 1
    assert snapshot.server_errors == 1
    assert snapshot.total_duration_ms == 60.0
    assert snapshot.average_duration_ms == 20.0
    assert snapshot.maximum_duration_ms == 30.0
    assert snapshot.requests_by_method == {
        "GET": 2,
        "POST": 1,
    }
    assert snapshot.requests_by_status == {
        "200": 1,
        "404": 1,
        "503": 1,
    }


def test_redirect_counts_as_successful_request() -> None:
    collector = HttpMetricsCollector()

    collector.record(
        method="GET",
        status_code=302,
        duration_ms=4.5,
    )

    snapshot = collector.snapshot()

    assert snapshot.successful_requests == 1
    assert snapshot.client_errors == 0
    assert snapshot.server_errors == 0


def test_negative_duration_is_normalized_to_zero() -> None:
    collector = HttpMetricsCollector()

    collector.record(
        method="GET",
        status_code=200,
        duration_ms=-5.0,
    )

    snapshot = collector.snapshot()

    assert snapshot.total_duration_ms == 0.0
    assert snapshot.average_duration_ms == 0.0
    assert snapshot.maximum_duration_ms == 0.0


def test_snapshot_returns_independent_dictionaries() -> None:
    collector = HttpMetricsCollector()
    collector.record(
        method="GET",
        status_code=200,
        duration_ms=1.0,
    )

    first_snapshot = collector.snapshot()
    first_snapshot.requests_by_method["POST"] = 99
    first_snapshot.requests_by_status["500"] = 99

    second_snapshot = collector.snapshot()

    assert second_snapshot.requests_by_method == {"GET": 1}
    assert second_snapshot.requests_by_status == {"200": 1}


def test_reset_clears_collector() -> None:
    collector = HttpMetricsCollector()
    collector.record(
        method="GET",
        status_code=500,
        duration_ms=15.0,
    )

    collector.reset()
    snapshot = collector.snapshot()

    assert snapshot.total_requests == 0
    assert snapshot.server_errors == 0
    assert snapshot.total_duration_ms == 0.0
    assert snapshot.requests_by_method == {}
    assert snapshot.requests_by_status == {}


def test_module_level_collector_functions() -> None:
    reset_http_metrics()

    record_http_request(
        method="GET",
        status_code=204,
        duration_ms=12.5,
    )

    snapshot = get_http_metrics()

    assert snapshot.total_requests == 1
    assert snapshot.successful_requests == 1
    assert snapshot.average_duration_ms == 12.5

    reset_http_metrics()


def test_request_context_middleware_records_successful_request() -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from tmb_ai_os.middleware import RequestContextMiddleware

    reset_http_metrics()

    app = FastAPI()
    app.add_middleware(RequestContextMiddleware)

    @app.get("/example")
    def example() -> dict[str, bool]:
        return {"ok": True}

    with TestClient(app) as client:
        response = client.get("/example")

    snapshot = get_http_metrics()

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]
    assert snapshot.total_requests == 1
    assert snapshot.successful_requests == 1
    assert snapshot.requests_by_method == {"GET": 1}
    assert snapshot.requests_by_status == {"200": 1}

    reset_http_metrics()


def test_request_context_middleware_records_server_exception() -> None:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from tmb_ai_os.middleware import RequestContextMiddleware

    reset_http_metrics()

    app = FastAPI()
    app.add_middleware(RequestContextMiddleware)

    @app.get("/failure")
    def failure() -> None:
        raise RuntimeError("expected test failure")

    with TestClient(
        app,
        raise_server_exceptions=False,
    ) as client:
        response = client.get("/failure")

    snapshot = get_http_metrics()

    assert response.status_code == 500
    assert snapshot.total_requests == 1
    assert snapshot.server_errors == 1
    assert snapshot.requests_by_method == {"GET": 1}
    assert snapshot.requests_by_status == {"500": 1}

    reset_http_metrics()


def test_http_metrics_api_returns_snapshot() -> None:
    from tmb_ai_os.api_v9 import http_request_metrics

    reset_http_metrics()
    record_http_request(
        method="POST",
        status_code=201,
        duration_ms=25.0,
    )

    result = http_request_metrics()

    assert result["total_requests"] == 1
    assert result["successful_requests"] == 1
    assert result["average_duration_ms"] == 25.0
    assert result["requests_by_method"] == {"POST": 1}
    assert result["requests_by_status"] == {"201": 1}

    reset_http_metrics()
