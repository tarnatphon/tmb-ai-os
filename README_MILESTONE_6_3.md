# TMB AI OS — Milestone 6.3: Scoped API Keys

This milestone adds fine-grained API key scopes and least-privilege access.

## Features

- Per-key scopes
- Scope validation
- Role-to-default-scope mapping
- Scope-aware authentication dependency
- API endpoints under `/v22`
- Migration guard for protected routes

## API

- `GET /v22/scopes`
- `GET /v22/api-keys/{key_id}/scopes`
- `PUT /v22/api-keys/{key_id}/scopes`

## Apply

```bash
python scripts/apply_milestone_6_3.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
