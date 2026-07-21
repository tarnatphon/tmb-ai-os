from .http_metrics import HttpMetricsSnapshot


def _escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def render_prometheus_metrics(snapshot: HttpMetricsSnapshot) -> str:
    lines = [
        "# HELP tmb_http_requests_total Total number of HTTP requests.",
        "# TYPE tmb_http_requests_total counter",
        f"tmb_http_requests_total {snapshot.total_requests}",
        "# HELP tmb_http_successful_requests_total HTTP requests with 2xx or 3xx status.",
        "# TYPE tmb_http_successful_requests_total counter",
        f"tmb_http_successful_requests_total {snapshot.successful_requests}",
        "# HELP tmb_http_client_errors_total HTTP requests with 4xx status.",
        "# TYPE tmb_http_client_errors_total counter",
        f"tmb_http_client_errors_total {snapshot.client_errors}",
        "# HELP tmb_http_server_errors_total HTTP requests with 5xx status.",
        "# TYPE tmb_http_server_errors_total counter",
        f"tmb_http_server_errors_total {snapshot.server_errors}",
        "# HELP tmb_http_request_duration_milliseconds_total Total HTTP request duration.",
        "# TYPE tmb_http_request_duration_milliseconds_total counter",
        (f"tmb_http_request_duration_milliseconds_total {snapshot.total_duration_ms}"),
        "# HELP tmb_http_request_duration_milliseconds_average Average HTTP request duration.",
        "# TYPE tmb_http_request_duration_milliseconds_average gauge",
        (f"tmb_http_request_duration_milliseconds_average {snapshot.average_duration_ms}"),
        "# HELP tmb_http_request_duration_milliseconds_maximum Maximum HTTP request duration.",
        "# TYPE tmb_http_request_duration_milliseconds_maximum gauge",
        (f"tmb_http_request_duration_milliseconds_maximum {snapshot.maximum_duration_ms}"),
        "# HELP tmb_http_requests_by_method_total HTTP requests grouped by method.",
        "# TYPE tmb_http_requests_by_method_total counter",
    ]

    for method, count in sorted(snapshot.requests_by_method.items()):
        escaped_method = _escape_label(method)
        lines.append(f'tmb_http_requests_by_method_total{{method="{escaped_method}"}} {count}')

    lines.extend(
        [
            "# HELP tmb_http_requests_by_status_total HTTP requests grouped by status.",
            "# TYPE tmb_http_requests_by_status_total counter",
        ]
    )

    for status, count in sorted(snapshot.requests_by_status.items()):
        escaped_status = _escape_label(status)
        lines.append(f'tmb_http_requests_by_status_total{{status="{escaped_status}"}} {count}')

    return "\n".join(lines) + "\n"
