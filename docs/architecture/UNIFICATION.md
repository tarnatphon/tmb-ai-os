# Architecture Unification

## Canonical package

All new production code belongs in:

```text
src/tmb_ai_os/
```

## Legacy package

The `app/` package is transitional. It must not receive new business logic.

Allowed uses:

- Compatibility imports
- Temporary adapters
- Transitional wrappers

Disallowed uses:

- New domain models
- New providers
- New workflows
- New agents
- New content logic

## Entry points

Canonical:

```text
tmb_ai_os.main:app
```

Compatibility:

```text
app.main:app
```
