# Sprint 1A — Enterprise Foundation

## Scope

This increment establishes an executable modular monolith. It intentionally uses in-process
infrastructure so local development remains simple while interfaces are prepared for later
replacement by PostgreSQL, Redis, and a durable message broker.

## Components

- `Settings`: immutable environment configuration
- `EventBus`: asynchronous pub/sub contract
- `JobQueue`: priority jobs and retry bookkeeping
- `PluginRegistry`: YAML manifest discovery and validation
- `AuditTrail`: immutable audit record model
- `Runtime`: dependency container shared by the API
- `FastAPI`: health and plugin discovery endpoints

## Security decisions

- Secrets are never committed; `.env.example` contains names only.
- Plugin manifests declare permissions before executable loading is introduced.
- CI runs dependency audit and secret scanning.
- No automatic remote registration, CAPTCHA bypass, or uncontrolled publishing is included.

## Next increment

Sprint 1B will add PostgreSQL persistence, identity/RBAC, durable audit storage, Redis-backed
jobs, migrations, and API authentication while preserving these public interfaces.
