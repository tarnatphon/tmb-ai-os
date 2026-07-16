# TMB AI OS — Milestone 6.1: Multi-Key Management

This milestone replaces the single-key model with managed API keys.

## Features

- Multiple API keys
- SHA-256 key hashing
- Key IDs
- Role assignment
- Expiration
- Revocation
- Key rotation
- Admin-only management API under `/v20`

## API

- `POST /v20/api-keys`
- `GET /v20/api-keys`
- `POST /v20/api-keys/{key_id}/revoke`
- `POST /v20/api-keys/{key_id}/rotate`

## Apply

```bash
python scripts/apply_milestone_6_1.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
