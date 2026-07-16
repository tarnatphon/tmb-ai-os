# TMB AI OS — Milestone 5.7: Alerts & Incident Tracking

This milestone adds operational alerting and incident tracking.

## Features

- Alert rules for health, publish queue, backup, and maintenance
- Incident persistence
- Webhook notifier interface
- Dry-run notifier
- Alert evaluation API under `/v16`
- Incident acknowledgement and resolution

## API

- `POST /v16/alerts/evaluate`
- `GET /v16/incidents`
- `POST /v16/incidents/{incident_id}/acknowledge`
- `POST /v16/incidents/{incident_id}/resolve`

## Apply

```bash
python scripts/apply_milestone_5_7.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
