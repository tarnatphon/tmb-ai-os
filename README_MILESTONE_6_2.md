# TMB AI OS — Milestone 6.2: Unified Authentication Migration

This milestone migrates protected APIs from the legacy environment API key
to managed database-backed API keys.

## Features

- Unified authentication dependency
- Managed API key first, legacy key fallback
- Optional legacy fallback disable flag
- Authentication audit logging
- Dashboard and admin API migration
- Migration status endpoint under `/v21`

## API

- `GET /v21/auth/status`
- `POST /v21/auth/validate`

## Apply

```bash
python scripts/apply_milestone_6_2.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
