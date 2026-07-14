# TMB AI OS — Milestone 4.4: Database, Models & Scheduler Migration

This milestone moves persistence and scheduling ownership into `src/tmb_ai_os`.

## Canonical modules

- `tmb_ai_os.database`
- `tmb_ai_os.models`
- `tmb_ai_os.scheduler`

## Compatibility wrappers

The following legacy modules become thin wrappers:

- `app.core.database`
- `app.core.models`
- `app.services.scheduler`

Original implementations are backed up before replacement.

## Apply

```bash
python scripts/apply_milestone_4_4_all.py
```

## Validate

```bash
python scripts/check_legacy_callsites.py
python scripts/audit_legacy_dependencies.py
ruff format .
ruff check .
mypy src
pytest
```

## Runtime

Canonical application:

```bash
uvicorn tmb_ai_os.main:app --reload
```

The application lifespan initializes database tables and starts the scheduler
only when `TMB_SCHEDULER_ENABLED=true`.
