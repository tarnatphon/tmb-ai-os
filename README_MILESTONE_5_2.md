# TMB AI OS — Milestone 5.2: Security Hardening

This milestone adds operational security controls around the API.

## Features

- Request IDs
- Structured request logging
- In-memory rate limiting
- Security response headers
- Startup secret validation
- API endpoints under `/v11`

## API

- `GET /v11/security/config`
- `GET /v11/security/rate-limit`

## Apply

```bash
python scripts/apply_milestone_5_2.py
```

## Environment

```env
TMB_RATE_LIMIT_REQUESTS=60
TMB_RATE_LIMIT_WINDOW_SECONDS=60
TMB_REQUIRE_SECURE_API_KEY=true
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
