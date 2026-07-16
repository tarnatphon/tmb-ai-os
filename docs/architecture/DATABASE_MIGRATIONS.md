# Database Migrations

Apply:
```bash
alembic upgrade head
```

Check:
```bash
python scripts/check_migration_status.py
```

PostgreSQL:
```env
TMB_DATABASE_URL=postgresql+psycopg://user:password@host:5432/tmb_ai_os
```
