# TMB AI OS — Milestone 4: Architecture Unification

This milestone consolidates the project around a single application core:

```text
src/tmb_ai_os/
```

The legacy `app/` package remains as a thin compatibility layer during migration.

## Canonical entry point

```bash
uvicorn tmb_ai_os.main:app --reload
```

Legacy compatibility entry point:

```bash
uvicorn app.main:app --reload
```

## Apply

```bash
python scripts/apply_milestone_4.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
```
