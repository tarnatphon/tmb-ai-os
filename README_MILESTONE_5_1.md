# TMB AI OS — Milestone 5.1: API Security & RBAC

This milestone adds authentication and role-based access control.

## Features

- API key authentication
- Roles: viewer, reviewer, manager, publisher, admin
- Permission checks
- Security audit events
- Protected operational endpoints
- API endpoints under `/v10`

## API

- `GET /v10/security/me`
- `GET /v10/security/roles`
- `GET /v10/security/audit`

## Apply

```bash
python scripts/apply_milestone_5_1.py
```

## Environment

```env
TMB_API_KEY=change-me
TMB_API_ROLE=admin
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
