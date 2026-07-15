# TMB AI OS — Milestone 4.8: Publisher Adapters & Queue Worker

This milestone adds a safe publishing execution layer.

## Features

- Publisher protocol
- Dry-run publisher for local testing
- Publish queue processor
- Idempotent queue execution
- Queue item status updates
- Publish audit events
- API endpoints under `/v7`

## API

- `POST /v7/publish-queue/process`
- `GET /v7/publishers`
- `GET /v7/publish-queue/{queue_id}`

## Safety

No real social platform integration is enabled in this milestone.
The default publisher is `dry_run`, which records a simulated publish result.

## Apply

```bash
python scripts/apply_milestone_4_8.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
