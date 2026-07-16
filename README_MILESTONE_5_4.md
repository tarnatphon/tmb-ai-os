# TMB AI OS — Milestone 5.4: Alembic & PostgreSQL Readiness

Features:
- Alembic configuration
- Initial canonical schema migration
- Migration status checks
- PostgreSQL-compatible settings
- API endpoints under `/v13`

Apply:
```bash
python scripts/apply_milestone_5_4.py
pip install -e ".[dev]"
alembic upgrade head
```

Validate:
```bash
ruff format .
ruff check .
mypy src
pytest
```
