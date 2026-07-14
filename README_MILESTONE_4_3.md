# TMB AI OS — Milestone 4.3: Legacy Call-Site Migration

This milestone migrates project call sites away from the transitional wrappers:

- `app.core.config`
- `app.providers.base`
- `app.providers.factory`

The wrappers remain temporarily for external compatibility, but internal
application code should import canonical modules directly.

## Apply

```bash
python scripts/migrate_legacy_callsites.py
```

Preview changes without writing:

```bash
python scripts/migrate_legacy_callsites.py --check
```

Audit:

```bash
python scripts/check_legacy_callsites.py
python scripts/audit_legacy_dependencies.py
```

Validate:

```bash
ruff format .
ruff check .
mypy src
pytest
```

## Success criteria

- Canonical to legacy dependencies remain zero.
- No internal Python file imports the three migrated legacy modules,
  except the compatibility wrappers themselves and migration backups.
- Existing wrappers remain available for external callers.
