# TMB AI OS — Milestone 4.2: Config & Provider Migration

This milestone consolidates configuration and provider creation into
`src/tmb_ai_os`.

## Canonical modules

- `tmb_ai_os.config`
- `tmb_ai_os.provider_factory`
- `tmb_ai_os.provider_contracts`
- `tmb_ai_os.provider_adapter`
- `tmb_ai_os.providers`

## Apply

```bash
python scripts/apply_milestone_4_2_all.py
```

## Validate

```bash
python scripts/audit_legacy_dependencies.py
ruff format .
ruff check .
mypy src
pytest
```

Legacy files are backed up before wrappers are installed.
