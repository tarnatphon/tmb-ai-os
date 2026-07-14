# Config and Provider Migration

Canonical ownership:

```text
tmb_ai_os.config
tmb_ai_os.provider_factory
tmb_ai_os.provider_contracts
tmb_ai_os.provider_adapter
```

Legacy modules under `app/` are temporary compatibility wrappers.

Rollback:

```bash
python scripts/rollback_milestone_4_2.py
```
