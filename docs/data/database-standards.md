---
title: Database Standards
phase: "0.3"
status: approved
owner: platform-architecture
last_updated: 2026-07-30
tags: [database, postgresql, standards, migrations]
---

# Database Standards

## Scope

These standards apply to all PostgreSQL schemas, migrations, queries, indexes, and operational procedures in the TMB AI OS.

## Naming

- Use lowercase `snake_case`.
- Table names are plural nouns.
- Primary keys are named `id`.
- Foreign keys use `<entity>_id`.
- Tenant-owned tables include `tenant_id`.
- Timestamps use `_at`; dates use `_date`.
- Boolean columns use clear predicates such as `is_active`.

## Required Columns

Tenant-owned mutable records should normally include:

- `id`
- `tenant_id`
- `created_at`
- `updated_at`
- optional `created_by`
- optional `updated_by`

Use timezone-aware UTC timestamps.

## Keys and Identifiers

Use stable globally unique identifiers for externally visible resources. Never expose sequential identifiers where enumeration creates security or privacy risk.

Foreign keys must define intentional update and deletion behavior. Cascading deletion requires explicit review.

## Constraints

Enforce invariants at the database layer where practical:

- `NOT NULL`
- unique constraints
- foreign keys
- check constraints
- valid status values
- tenant-aware uniqueness

Application validation does not replace database constraints.

## Indexes

Indexes must support verified query patterns. Every index adds write and storage cost and therefore requires a documented purpose.

Common candidates include:

- foreign keys
- tenant-scoped lookups
- status and date filters
- idempotency keys
- event processing state
- audit timestamps

Avoid indexing secrets or unnecessary sensitive values.

## Queries

- Always parameterize input.
- Never construct SQL from untrusted strings.
- Scope tenant-owned queries by `tenant_id`.
- Set explicit limits for list endpoints.
- Avoid unbounded scans and N+1 patterns.
- Use transactions for multi-step state changes.
- Apply lock timeouts and statement timeouts appropriate to the workload.

## Migrations

Every schema change must be represented by a version-controlled migration.

A migration must be:

- deterministic
- reviewable
- tested on representative data
- backward-compatible during rolling deployment where required
- safe to retry or clearly guarded
- accompanied by rollback or recovery guidance

Destructive migrations use an expand-migrate-contract sequence. Data backfills run in bounded batches and expose progress telemetry.

## Secrets

Credentials are never committed to the repository. Applications receive credentials through approved secret management and use least-privilege database roles.

## Roles

Separate roles should exist for:

- migrations
- application runtime
- read-only reporting
- backup and restoration
- operational administration

Production superuser access is exceptional, time-bound, and audited.

## Testing

Database changes require automated tests for migrations, constraints, tenant isolation, authorization-sensitive queries, and important query plans.

## Production Operations

- Enable encrypted connections.
- Restrict network access.
- Monitor slow queries and connection saturation.
- Test backups and restoration.
- Review unused indexes.
- Vacuum and analyze according to workload.
- Maintain documented emergency procedures.
