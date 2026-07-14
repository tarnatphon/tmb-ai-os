# Legacy Migration Policy

## Dependency direction

Allowed during transition:

```text
app.* -> tmb_ai_os.*
```

Forbidden:

```text
tmb_ai_os.* -> app.*
```

The canonical package must remain independently deployable.

## Safe migration process

For each legacy module:

1. Audit all import sites.
2. Compare public APIs and settings contracts.
3. Add canonical tests.
4. Introduce a compatibility wrapper.
5. Update callers.
6. Verify that no legacy imports remain.
7. Delete implementation only after CI passes.

## Current priorities

- `app.core.config`
- `app.providers.base`
- `app.providers.factory`
- Legacy content and scheduler services
