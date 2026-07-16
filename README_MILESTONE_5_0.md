# TMB AI OS — Milestone 5.0: Observability & Operations

Features:
- Liveness and readiness checks
- Database health check
- Scheduler status
- Publish queue metrics
- Content workflow metrics
- API endpoints under `/v9`

Apply:

```bash
python scripts/apply_milestone_5_0.py
```

Validate:

```bash
ruff format .
ruff check .
mypy src
pytest
```
