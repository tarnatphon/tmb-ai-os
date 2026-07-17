# TMB AI OS — Milestone 6.6: API Key Lifecycle

Adds lifecycle policy, expiry enforcement, forced rotation, revocation,
risk reporting, tests, and CI validation.

## Apply

```bash
python scripts/apply_milestone_6_6.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
python scripts/check_api_key_lifecycle.py
```
