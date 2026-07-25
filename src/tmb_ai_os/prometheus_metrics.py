from tmb_ai_os.alert_observability import AlertMetricsSnapshot
from tmb_ai_os.http_metrics import HttpMetricsSnapshot
from tmb_ai_os.operations_metrics import (
    AgentMetrics,
    AiMetrics,
    OperationsMetrics,
    WorkflowMetrics,
)


def _escape_label(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')


def _render_http_metrics(snapshot: HttpMetricsSnapshot) -> list[str]:
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
        f"tmb_http_request_duration_milliseconds_total {snapshot.total_duration_ms}",
        "# HELP tmb_http_request_duration_milliseconds_average Average HTTP request duration.",
        "# TYPE tmb_http_request_duration_milliseconds_average gauge",
        f"tmb_http_request_duration_milliseconds_average {snapshot.average_duration_ms}",
        "# HELP tmb_http_request_duration_milliseconds_maximum Maximum HTTP request duration.",
        "# TYPE tmb_http_request_duration_milliseconds_maximum gauge",
        f"tmb_http_request_duration_milliseconds_maximum {snapshot.maximum_duration_ms}",
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

    return lines


def _render_alert_metrics(snapshot: AlertMetricsSnapshot) -> list[str]:
    return [
        "# HELP tmb_alerts_routed_total Total number of alerts processed by the router.",
        "# TYPE tmb_alerts_routed_total counter",
        f"tmb_alerts_routed_total {snapshot.routed_total}",
        "# HELP tmb_alert_delivery_success_total Successful alert delivery attempts.",
        "# TYPE tmb_alert_delivery_success_total counter",
        f"tmb_alert_delivery_success_total {snapshot.delivery_success_total}",
        "# HELP tmb_alert_delivery_failed_total Failed alert delivery attempts.",
        "# TYPE tmb_alert_delivery_failed_total counter",
        f"tmb_alert_delivery_failed_total {snapshot.delivery_failed_total}",
        "# HELP tmb_alert_delivery_suppressed_total Suppressed alert delivery attempts.",
        "# TYPE tmb_alert_delivery_suppressed_total counter",
        f"tmb_alert_delivery_suppressed_total {snapshot.delivery_suppressed_total}",
        "# HELP tmb_alert_fallback_total Alerts that required fallback delivery.",
        "# TYPE tmb_alert_fallback_total counter",
        f"tmb_alert_fallback_total {snapshot.fallback_total}",
        "# HELP tmb_alert_no_route_total Alerts with no configured delivery route.",
        "# TYPE tmb_alert_no_route_total counter",
        f"tmb_alert_no_route_total {snapshot.no_route_total}",
    ]


def _render_ai_metrics(snapshot: AiMetrics) -> list[str]:
    return [
        "# HELP tmb_ai_requests_total Total number of AI requests.",
        "# TYPE tmb_ai_requests_total counter",
        f"tmb_ai_requests_total {snapshot.requests}",
        "# HELP tmb_ai_input_tokens_total Total number of AI input tokens.",
        "# TYPE tmb_ai_input_tokens_total counter",
        f"tmb_ai_input_tokens_total {snapshot.input_tokens}",
        "# HELP tmb_ai_output_tokens_total Total number of AI output tokens.",
        "# TYPE tmb_ai_output_tokens_total counter",
        f"tmb_ai_output_tokens_total {snapshot.output_tokens}",
        "# HELP tmb_ai_cost_usd_total Estimated AI cost in US dollars.",
        "# TYPE tmb_ai_cost_usd_total counter",
        f"tmb_ai_cost_usd_total {snapshot.estimated_cost_usd}",
    ]


def _render_agent_metrics(snapshot: AgentMetrics) -> list[str]:
    return [
        "# HELP tmb_agent_runs_total Total number of AI agent runs.",
        "# TYPE tmb_agent_runs_total counter",
        f"tmb_agent_runs_total {snapshot.total_runs}",
        "# HELP tmb_agent_successful_runs_total Successful AI agent runs.",
        "# TYPE tmb_agent_successful_runs_total counter",
        f"tmb_agent_successful_runs_total {snapshot.successful_runs}",
        "# HELP tmb_agent_failed_runs_total Failed AI agent runs.",
        "# TYPE tmb_agent_failed_runs_total counter",
        f"tmb_agent_failed_runs_total {snapshot.failed_runs}",
    ]


def _render_workflow_metrics(snapshot: WorkflowMetrics) -> list[str]:
    return [
        "# HELP tmb_workflow_runs_total Total number of workflow runs.",
        "# TYPE tmb_workflow_runs_total counter",
        f"tmb_workflow_runs_total {snapshot.total_runs}",
        "# HELP tmb_workflow_active_runs Current active workflow runs.",
        "# TYPE tmb_workflow_active_runs gauge",
        f"tmb_workflow_active_runs {snapshot.active_runs}",
        "# HELP tmb_workflow_failed_runs_total Failed workflow runs.",
        "# TYPE tmb_workflow_failed_runs_total counter",
        f"tmb_workflow_failed_runs_total {snapshot.failed_runs}",
    ]


def _render_operations_metrics(snapshot: OperationsMetrics) -> list[str]:
    lines = _render_ai_metrics(snapshot.ai)
    lines.extend(_render_agent_metrics(snapshot.agents))
    lines.extend(_render_workflow_metrics(snapshot.workflows))
    return lines


def render_prometheus_metrics(
    snapshot: HttpMetricsSnapshot,
    alert_snapshot: AlertMetricsSnapshot | None = None,
    operations_snapshot: OperationsMetrics | None = None,
) -> str:
    lines = _render_http_metrics(snapshot)

    if alert_snapshot is not None:
        lines.extend(_render_alert_metrics(alert_snapshot))

    if operations_snapshot is not None:
        lines.extend(_render_operations_metrics(operations_snapshot))

    return "\n".join(lines) + "\n"
