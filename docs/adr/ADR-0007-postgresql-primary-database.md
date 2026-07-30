---
title: ADR-0007 PostgreSQL as Primary Database
status: accepted
date: 2026-07-30
decision_owners: [platform-architecture]
tags: [adr, postgresql, database]
---

# ADR-0007: PostgreSQL as the Primary Database

## Context

The platform needs transactional integrity, tenant-aware relational queries, constraints, migrations, auditability, and mature operational tooling.

## Decision

PostgreSQL will be the primary transactional database and system of record for structured platform data.

Object storage, caches, search indexes, and vector stores may be used for specialized workloads, but they remain derived or purpose-specific systems unless a later ADR states otherwise.

## Consequences

### Positive

- strong transactions and constraints
- mature backup and recovery
- broad tooling and ecosystem support
- Row-Level Security capability
- JSON support where limited flexibility is needed
- reliable migration practices

### Negative

- scaling and query design require discipline
- specialized workloads may require additional stores
- operational expertise is required

## Guardrails

- tenant-owned records include `tenant_id`
- least-privilege roles
- encrypted connections
- version-controlled migrations
- tested backup and restoration
- query and index monitoring
- no uncontrolled direct external access

## Status

Accepted.
