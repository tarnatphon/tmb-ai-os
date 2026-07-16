# TMB AI OS — Milestone 5.6: Data Retention & Maintenance

This milestone adds safe retention and housekeeping capabilities.

## Features

- Retention policies for content, audit logs, and backups
- Cleanup preview mode
- Confirmed purge mode
- Maintenance summary
- API endpoints under `/v15`
- Scheduled maintenance command

## API

- `GET /v15/maintenance/preview`
- `POST /v15/maintenance/run`
- `GET /v15/maintenance/config`

## Apply

```bash
python scripts/apply_milestone_5_6.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
