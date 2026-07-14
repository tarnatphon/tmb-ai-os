# TMB AI OS — Milestone 4.1: Legacy Dependency Audit

This milestone prepares the safe removal of duplicated legacy modules.

## Objectives

- Detect imports that still reference `app.*`
- Detect imports from canonical code back into the legacy package
- Produce a machine-readable migration report
- Add CI tests that prevent new canonical-to-legacy dependencies
- Create a migration manifest for duplicated modules

## Apply

```bash
cp -R /path/to/tmb-ai-os-milestone-4-1-legacy-audit/. .
```

Run the audit:

```bash
python scripts/audit_legacy_dependencies.py
```

Write JSON report:

```bash
python scripts/audit_legacy_dependencies.py \
  --json reports/legacy-dependencies.json
```

Validate:

```bash
ruff format .
ruff check .
mypy src
pytest
```

## Migration policy

Canonical code under `src/tmb_ai_os` must never import `app.*`.

Legacy code may temporarily import canonical code during migration.

The next phase will use the report to migrate:

1. `app/core/config.py`
2. `app/providers/base.py`
3. `app/providers/factory.py`
4. Remaining legacy-only services
