# Database, Models and Scheduler Migration

Canonical ownership:

```text
tmb_ai_os.database
tmb_ai_os.models
tmb_ai_os.scheduler
tmb_ai_os.lifecycle
```

The canonical FastAPI lifespan initializes database tables and conditionally
starts the background scheduler.

Scheduler defaults to disabled. Enable it explicitly:

```env
TMB_SCHEDULER_ENABLED=true
TMB_SCHEDULER_HOUR=8
TMB_SCHEDULER_MINUTE=0
TMB_APP_TIMEZONE=Asia/Bangkok
```

Rollback:

```bash
python scripts/rollback_milestone_4_4.py
```
