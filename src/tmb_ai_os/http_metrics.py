from dataclasses import dataclass, field
from threading import Lock


@dataclass(frozen=True)
class HttpMetricsSnapshot:
    total_requests: int
    successful_requests: int
    client_errors: int
    server_errors: int
    total_duration_ms: float
    average_duration_ms: float
    maximum_duration_ms: float
    requests_by_method: dict[str, int] = field(default_factory=dict)
    requests_by_status: dict[str, int] = field(default_factory=dict)


class HttpMetricsCollector:
    def __init__(self) -> None:
        self._lock = Lock()
        self._total_requests = 0
        self._successful_requests = 0
        self._client_errors = 0
        self._server_errors = 0
        self._total_duration_ms = 0.0
        self._maximum_duration_ms = 0.0
        self._requests_by_method: dict[str, int] = {}
        self._requests_by_status: dict[str, int] = {}

    def record(
        self,
        *,
        method: str,
        status_code: int,
        duration_ms: float,
    ) -> None:
        normalized_method = method.upper()
        normalized_status = str(status_code)
        safe_duration_ms = max(0.0, duration_ms)

        with self._lock:
            self._total_requests += 1
            self._total_duration_ms += safe_duration_ms
            self._maximum_duration_ms = max(
                self._maximum_duration_ms,
                safe_duration_ms,
            )

            self._requests_by_method[normalized_method] = (
                self._requests_by_method.get(normalized_method, 0) + 1
            )
            self._requests_by_status[normalized_status] = (
                self._requests_by_status.get(normalized_status, 0) + 1
            )

            if 200 <= status_code < 400:
                self._successful_requests += 1
            elif 400 <= status_code < 500:
                self._client_errors += 1
            elif status_code >= 500:
                self._server_errors += 1

    def snapshot(self) -> HttpMetricsSnapshot:
        with self._lock:
            average_duration_ms = (
                self._total_duration_ms / self._total_requests if self._total_requests else 0.0
            )

            return HttpMetricsSnapshot(
                total_requests=self._total_requests,
                successful_requests=self._successful_requests,
                client_errors=self._client_errors,
                server_errors=self._server_errors,
                total_duration_ms=round(self._total_duration_ms, 2),
                average_duration_ms=round(average_duration_ms, 2),
                maximum_duration_ms=round(self._maximum_duration_ms, 2),
                requests_by_method=dict(self._requests_by_method),
                requests_by_status=dict(self._requests_by_status),
            )

    def reset(self) -> None:
        with self._lock:
            self._total_requests = 0
            self._successful_requests = 0
            self._client_errors = 0
            self._server_errors = 0
            self._total_duration_ms = 0.0
            self._maximum_duration_ms = 0.0
            self._requests_by_method.clear()
            self._requests_by_status.clear()


http_metrics_collector = HttpMetricsCollector()


def record_http_request(
    *,
    method: str,
    status_code: int,
    duration_ms: float,
) -> None:
    http_metrics_collector.record(
        method=method,
        status_code=status_code,
        duration_ms=duration_ms,
    )


def get_http_metrics() -> HttpMetricsSnapshot:
    return http_metrics_collector.snapshot()


def reset_http_metrics() -> None:
    http_metrics_collector.reset()
