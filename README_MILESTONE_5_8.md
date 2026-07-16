# TMB AI OS — Milestone 5.8: Webhook Notifications & Escalation

This milestone adds real webhook delivery and incident escalation.

## Features

- Signed webhook notifications
- Delivery logs
- Retry policy
- Escalation levels
- Dry-run and webhook notifier support
- API endpoints under `/v17`

## API

- `POST /v17/notifications/test`
- `GET /v17/notifications/deliveries`
- `POST /v17/incidents/{incident_id}/escalate`

## Apply

```bash
python scripts/apply_milestone_5_8.py
```

## Environment

```env
TMB_WEBHOOK_URL=
TMB_WEBHOOK_SECRET=
TMB_NOTIFICATION_PROVIDER=dry_run
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
