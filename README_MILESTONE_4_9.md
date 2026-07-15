# TMB AI OS — Milestone 4.9: Scheduled Publishing & Retry Policy

This milestone adds scheduled publishing and resilient queue processing.

## Features

- Schedule publish queue items
- Process only due items
- Retry failed publishes
- Exponential backoff
- Failed and retrying states
- Maximum attempt limits
- Dry-run compatible
- API endpoints under `/v8`

## API

- `POST /v8/publish-queue/{queue_id}/schedule`
- `POST /v8/publish-queue/process-due`
- `GET /v8/publish-queue/failed`

## Apply

```bash
python scripts/apply_milestone_4_9.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
