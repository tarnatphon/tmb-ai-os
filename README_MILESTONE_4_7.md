# TMB AI OS — Milestone 4.7: Approval Workflow & Publish Queue

This milestone adds editorial approval and publishing queue capabilities.

## Features

- Review content
- Approve or reject content
- Queue approved content for publishing
- Track audit events
- Prevent invalid status transitions
- Expose workflow APIs under `/v6`

## API

- `POST /v6/content/{content_id}/review`
- `POST /v6/content/{content_id}/approve`
- `POST /v6/content/{content_id}/reject`
- `POST /v6/content/{content_id}/publish`
- `GET /v6/publish-queue`
- `GET /v6/content/{content_id}/audit`

## Apply

```bash
python scripts/apply_milestone_4_7.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
