# Observability and Operations

Health:

```text
GET /v9/health/live
GET /v9/health/ready
```

Metrics:

```text
GET /v9/metrics/operations
GET /v9/metrics/publish-queue
GET /v9/metrics/content
```

## Prometheus metrics

The Prometheus endpoint exposes HTTP, alert, AI, agent, and workflow metrics using the Prometheus text exposition format.

Endpoint: `GET /v9/metrics/prometheus`

Example: `curl http://localhost:8000/v9/metrics/prometheus`

Response media type: `text/plain; version=0.0.4`

### AI metrics

- `tmb_ai_requests_total`
- `tmb_ai_input_tokens_total`
- `tmb_ai_output_tokens_total`
- `tmb_ai_cost_usd_total`

### Agent metrics

- `tmb_agent_runs_total`
- `tmb_agent_successful_runs_total`
- `tmb_agent_failed_runs_total`

### Workflow metrics

- `tmb_workflow_runs_total`
- `tmb_workflow_active_runs`
- `tmb_workflow_failed_runs_total`
