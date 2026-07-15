# TMB AI OS — Milestone 4.6: Generate-and-Persist Workflow

This milestone connects the multi-channel generator to canonical persistence.

## Features

- Generate content from a Markdown brief
- Persist channel outputs automatically
- Compute deterministic prompt hashes
- Prevent duplicate storage
- Expose workflow status
- Support preview mode without calling Gemini

## API

- `POST /v5/content/preview`
- `POST /v5/content/generate`
- `GET /v5/content/{content_id}/status`

## Apply

```bash
python scripts/apply_milestone_4_6.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
