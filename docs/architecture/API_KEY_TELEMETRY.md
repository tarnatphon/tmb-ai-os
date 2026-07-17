# API Key Telemetry

Milestone 6.7 records API key usage and calculates a risk score.

Risk signals:

- High request volume
- Elevated or high failure ratio
- Requests from many distinct IP addresses

API:

```text
GET /v26/security/api-key-telemetry/{api_key_id}/risk
GET /v26/security/api-key-telemetry/{api_key_id}/events
```

The middleware is provided separately and is not installed
automatically, avoiding changes to the existing authentication flow.
