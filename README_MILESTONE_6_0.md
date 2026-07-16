# TMB AI OS — Milestone 6.0: Secure Admin Dashboard & RBAC

This milestone secures the operations dashboard and administrative APIs.

## Features

- API-key protected admin dashboard
- Admin-only dashboard API routes
- Role-based access control integration
- Admin access audit events
- Login page for API key entry
- Session token stored in browser session storage
- API endpoints under `/v19`

## API

- `GET /v19/admin/session`
- `POST /v19/admin/audit`
- `GET /admin/login`
- `GET /admin`

## Apply

```bash
python scripts/apply_milestone_6_0.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
