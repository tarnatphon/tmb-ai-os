# ruff: noqa: E501
#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

DOCUMENTS = {
    "docs/data/data-architecture.md": """---
title: Data Architecture
phase: "0.3"
status: approved
owner: platform-architecture
last_updated: 2026-07-30
tags: [data, architecture, postgresql, multi-tenant]
---

# Data Architecture

## Purpose

This document defines the canonical data architecture for the TMB AI OS. The design prioritizes tenant isolation, security, auditability, predictable operations, and future growth.

## Architectural Principles

1. PostgreSQL is the primary transactional system of record.
2. Every tenant-owned record must carry an immutable `tenant_id`.
3. Services access data through documented repositories or APIs rather than direct cross-service table access.
4. Schema changes are version-controlled, reviewed, tested, and reversible.
5. Sensitive data is minimized, classified, encrypted, and access-controlled.
6. Operational events are published through versioned contracts.
7. Derived search indexes, caches, and vector stores are rebuildable from authoritative sources.

## Logical Data Domains

- Identity and access
- Tenant and organization
- Customer and sales
- Product and manufacturing
- Knowledge and content
- Agent and workflow
- Integration and webhook
- Audit and security telemetry

Each domain owns its schema, validation rules, retention requirements, and data access policy.

## Storage Components

### PostgreSQL

Used for transactional and relational data requiring integrity, constraints, joins, and durable audit trails.

### Object Storage

Used for large binary objects such as images, generated documents, exports, backups, and media. Database records store metadata and object references, not uncontrolled binary payloads.

### Vector Store

Used for RAG embeddings and semantic retrieval. Source documents, permissions, tenant identity, content version, and checksum must be preserved as metadata.

### Cache

Used only for rebuildable, time-bound acceleration. Cache entries must never become the sole authoritative record.

## Tenant Isolation

All tenant-owned tables must include `tenant_id`. Application queries must always scope by the authenticated tenant. Database policies such as PostgreSQL Row-Level Security should be used where practical as defense in depth.

Cross-tenant access is denied by default. Administrative access must be explicit, time-bound, audited, and limited to approved operational use cases.

## Data Lifecycle

Data passes through these stages:

1. Collection
2. Validation
3. Classification
4. Storage
5. Processing
6. Sharing or integration
7. Retention
8. Deletion or anonymization

Deletion must account for primary records, derived indexes, cached copies, object storage, backups, and downstream integrations.

## Consistency Model

Transactional workflows use database transactions and strong consistency. Distributed integrations use idempotency keys, retries, outbox patterns, and reconciliation jobs.

## Backup and Recovery

- Automated encrypted backups
- Point-in-time recovery where supported
- Regular restore testing
- Defined recovery time and recovery point objectives
- Tenant-aware incident procedures
- Backup access restricted to approved operators

## Observability

Data operations must emit structured logs and metrics without exposing secrets or unnecessary personal data. Required signals include migration status, query failures, lock contention, replication health, backup health, and restoration test results.

## Governance

Every new data domain must document ownership, purpose, classification, retention, tenant scope, authoritative source, and deletion behavior before production use.
""",
    "docs/data/database-standards.md": """---
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
""",
    "docs/data/data-classification.md": """---
title: Data Classification
phase: "0.3"
status: approved
owner: security
last_updated: 2026-07-30
tags: [data, classification, privacy, security]
---

# Data Classification

## Purpose

Classification determines how information is collected, stored, accessed, transmitted, logged, retained, and destroyed.

## Levels

### Public

Information approved for unrestricted publication.

Examples:

- published marketing content
- public product descriptions
- public documentation

Controls:

- integrity protection
- approved publication workflow

### Internal

Non-public business information with limited impact if disclosed.

Examples:

- internal procedures
- non-sensitive project plans
- ordinary operational metrics

Controls:

- authenticated access
- approved collaboration systems
- no uncontrolled public sharing

### Confidential

Information that could harm customers, tenants, employees, or the company if disclosed.

Examples:

- customer records
- quotations and contracts
- private business data
- unpublished product designs
- integration configuration

Controls:

- least-privilege access
- encryption in transit and at rest
- tenant isolation
- audited access
- approved retention and deletion

### Restricted

Highly sensitive data requiring the strongest safeguards.

Examples:

- passwords and password hashes
- API keys and signing secrets
- authentication tokens
- private keys
- sensitive personal data
- security incident evidence
- production backup credentials

Controls:

- approved secret manager or specialized storage
- strict role separation
- no plaintext logging
- short retention where possible
- access alerts and regular review
- emergency rotation and revocation procedures

## Handling Rules

The highest classification in a record, file, message, or dataset governs the entire object unless it is safely separated.

Data must not be copied into lower-control systems for convenience. Production data must not be used in development unless formally approved and appropriately minimized or anonymized.

## Logging

Logs must exclude secrets, complete tokens, passwords, private keys, sensitive request bodies, and unnecessary personal data. When identifiers are needed for diagnosis, use safe references or redacted values.

## AI and RAG

Before content enters an AI workflow or vector store:

1. Identify tenant ownership.
2. Determine classification.
3. Verify authorization.
4. Minimize sensitive fields.
5. Preserve source and permission metadata.
6. Define retention and deletion behavior.
7. Prevent cross-tenant retrieval.

Restricted secrets must never be embedded.

## Transmission

Confidential and Restricted data require encrypted transport. External sharing requires an approved purpose, recipient, minimum necessary content, and appropriate contractual or technical protection.

## Retention

Each domain must define a retention period based on operational, contractual, legal, and security needs. Data must not be retained indefinitely without justification.

## Incident Response

Suspected disclosure, cross-tenant access, secret exposure, or unauthorized processing must be reported and handled under the incident response process.
""",
    "docs/integrations/integration-architecture.md": """---
title: Integration Architecture
phase: "0.3"
status: approved
owner: platform-architecture
last_updated: 2026-07-30
tags: [integrations, api, events, connectors]
---

# Integration Architecture

## Purpose

This document defines how TMB AI OS connects with external services while preserving security, reliability, tenant isolation, and traceability.

## Integration Patterns

Supported patterns are:

- synchronous REST APIs
- outbound webhooks
- inbound webhooks
- scheduled import and export
- asynchronous events
- managed connectors
- file-based exchange through approved storage

The simplest pattern that satisfies the requirement should be selected.

## Integration Boundary

External systems never receive direct database access. All access passes through authenticated APIs, approved queues, signed webhooks, or controlled file exchange.

Each integration has an owner, tenant scope, data classification, credential strategy, rate limit, timeout, retry policy, and shutdown procedure.

## Connector Model

A connector must isolate:

- configuration
- credentials
- authentication
- request mapping
- response mapping
- retries
- rate limits
- health checks
- telemetry
- tenant identity

Provider-specific code must not leak into unrelated domain logic.

## Reliability

Integrations must define:

- connection and response timeouts
- bounded retries with backoff and jitter
- idempotency behavior
- duplicate handling
- dead-letter or failure handling
- reconciliation
- circuit breaking where appropriate

A remote success response does not always prove business completion; reconciliation is required for critical workflows.

## Security

Credentials are stored in approved secret management. Scopes must be minimal. Tokens are rotated and revocable. Sensitive payloads are minimized and encrypted in transit.

Inbound requests must authenticate the sender. Outbound requests must validate destinations and prevent server-side request forgery.

## Tenant Isolation

Every integration configuration belongs to a tenant unless explicitly platform-wide. Runtime processing carries tenant context end to end. Shared credentials require formal security review.

## Observability

Telemetry includes:

- provider
- connector
- tenant-safe identifier
- operation
- outcome
- latency
- retry count
- rate-limit state
- correlation ID

Logs must redact secrets and sensitive payloads.

## Change Management

Provider API versions and contract changes are tracked. Breaking changes require migration plans, compatibility testing, rollback guidance, and owner notification.

## Decommissioning

Disabling an integration includes revoking credentials, stopping schedules, draining pending work, preserving required audit data, deleting unnecessary cached data, and documenting the final state.
""",
    "docs/integrations/webhook-security.md": """---
title: Webhook Security
phase: "0.3"
status: approved
owner: security
last_updated: 2026-07-30
tags: [webhooks, security, signatures, replay-protection]
---

# Webhook Security

## Scope

These requirements apply to inbound and outbound webhooks.

## Transport

Webhook endpoints require HTTPS with modern TLS. Redirects are disabled unless explicitly required and validated.

## Authentication

Inbound webhooks must verify a cryptographic signature or an equivalent provider-supported authentication mechanism.

Preferred design:

- HMAC using SHA-256 or stronger
- signature calculated over the exact raw request body
- timestamp included in the signed material
- key identifier included where rotation is supported

Never trust source IP alone as the primary control.

## Replay Protection

Reject requests whose signed timestamp falls outside the allowed window. Store a delivery identifier, event identifier, or signature digest to detect duplicates.

Duplicate delivery should return a safe success response after confirming that the original event was accepted.

## Payload Handling

- Read the raw body before parsing.
- Enforce body-size limits.
- Validate content type.
- Validate schema and event type.
- Reject unknown or malformed payloads.
- Do not log secrets or complete sensitive payloads.
- Preserve a correlation identifier.

## Processing

A webhook endpoint should authenticate, validate, enqueue durable work, and respond quickly. Long-running business operations must not execute directly in the request handler.

Consumers must be idempotent.

## Secrets and Rotation

Signing secrets are stored in approved secret management. Rotation supports a defined overlap period with both current and previous keys where required.

Exposed or suspected secrets are revoked immediately and investigated.

## Outbound Webhooks

Outbound webhook destinations must be validated and protected against SSRF. Block private, loopback, link-local, metadata-service, and disallowed network ranges unless explicitly approved.

Outbound deliveries must include:

- event identifier
- event type
- timestamp
- contract version
- signature
- retry-safe semantics

## Retry Policy

Retry only transient failures. Use bounded exponential backoff with jitter. Permanent failures must enter a visible failure state or dead-letter process.

## Audit

Record delivery metadata, verification outcome, processing state, retry count, and final result. Audit records must avoid storing unnecessary sensitive content.
""",
    "docs/events/event-contracts.md": """---
title: Event Contracts
phase: "0.3"
status: approved
owner: platform-architecture
last_updated: 2026-07-30
tags: [events, contracts, versioning, async]
---

# Event Contracts

## Purpose

Event contracts provide a stable, versioned boundary for asynchronous communication.

## Event Envelope

Every event must include:

```json
{
  "event_id": "uuid",
  "event_type": "domain.entity.action",
  "event_version": 1,
  "occurred_at": "2026-07-30T00:00:00Z",
  "producer": "service-name",
  "tenant_id": "uuid",
  "correlation_id": "uuid",
  "causation_id": "uuid-or-null",
  "data": {}
}
```

## Naming

Use lower-case domain-oriented names:

`<domain>.<entity>.<past-tense-action>`

Examples:

- `sales.quotation.created`
- `knowledge.document.indexed`
- `workflow.run.failed`

Events describe facts that occurred, not commands.

## Versioning

`event_version` is an integer. Additive compatible changes may remain within the current version when consumers tolerate unknown fields. Breaking changes require a new version.

Published fields are not silently renamed, repurposed, or removed.

## Schema

Each event has a machine-readable schema stored in version control. The schema defines required fields, formats, enums, size limits, and compatibility rules.

## Tenant Context

Tenant-owned events require `tenant_id`. Producers derive it from trusted execution context, not from unchecked payload input.

Consumers must enforce tenant isolation before reading or changing state.

## Delivery Semantics

The platform assumes at-least-once delivery unless a component explicitly guarantees otherwise. Therefore:

- consumers are idempotent
- duplicates are expected
- ordering is not globally assumed
- retries are bounded and observable
- failed events have recovery procedures

## Sensitive Data

Events contain the minimum information required. Restricted secrets are prohibited. Confidential data requires documented justification and access controls.

Prefer identifiers and allow authorized consumers to retrieve details from the source API.

## Evolution

Contract changes require:

1. schema update
2. compatibility review
3. producer tests
4. consumer contract tests
5. migration guidance
6. deployment sequencing
7. rollback plan

## Observability

Track publication failures, consumer lag, processing latency, retries, duplicates, dead-letter volume, and schema validation failures.
""",
    "docs/adr/ADR-0006-api-first-design.md": """---
title: ADR-0006 API-First Design
status: accepted
date: 2026-07-30
decision_owners: [platform-architecture]
tags: [adr, api, architecture]
---

# ADR-0006: API-First Design

## Context

TMB AI OS includes web applications, agents, automation workflows, integrations, and future client applications. Direct coupling to internal implementation would make these clients difficult to secure and evolve.

## Decision

The platform will use an API-first design.

Public and service boundaries are defined through version-controlled contracts before implementation. Business capabilities are exposed through authenticated APIs or versioned events rather than direct database access.

## Consequences

### Positive

- consistent security controls
- reusable capabilities
- independent client development
- testable contracts
- clearer ownership
- controlled versioning

### Negative

- additional contract design work
- compatibility obligations
- need for API governance and documentation

## Guardrails

- OpenAPI or equivalent machine-readable definitions
- explicit authentication and authorization
- tenant context enforcement
- standard errors and pagination
- idempotency for retryable writes
- versioning and deprecation policy
- contract and security testing

## Status

Accepted.
""",
    "docs/adr/ADR-0007-postgresql-primary-database.md": """---
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
""",
    "docs/adr/ADR-0008-versioned-event-contracts.md": """---
title: ADR-0008 Versioned Event Contracts
status: accepted
date: 2026-07-30
decision_owners: [platform-architecture]
tags: [adr, events, versioning]
---

# ADR-0008: Versioned Event Contracts

## Context

Asynchronous workflows and integrations can fail when producers and consumers evolve independently without explicit compatibility rules.

## Decision

All platform events will use documented, machine-readable, versioned contracts and a standard event envelope.

Consumers must tolerate duplicate delivery and follow defined compatibility rules.

## Consequences

### Positive

- safer independent deployment
- clearer debugging and ownership
- contract testing
- predictable migration paths
- improved audit and observability

### Negative

- schema governance overhead
- consumers must support idempotency
- breaking changes require coordinated migration

## Guardrails

- immutable event meaning
- integer contract version
- schema stored in version control
- tenant context included where applicable
- no restricted secrets in events
- at-least-once delivery assumptions
- dead-letter and replay procedures
- producer and consumer contract tests

## Status

Accepted.
""",
}


def write_documents(force: bool) -> int:
    created = 0
    skipped = 0

    for filename, content in DOCUMENTS.items():
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)

        if path.exists() and path.stat().st_size > 0 and not force:
            print(f"SKIP  {filename} (already contains content)")
            skipped += 1
            continue

        path.write_text(content.rstrip() + "\n", encoding="utf-8")
        print(f"WRITE {filename}")
        created += 1

    print(f"\nWritten: {created}")
    print(f"Skipped: {skipped}")
    return 0


def validate() -> int:
    missing = []
    empty = []

    for filename in DOCUMENTS:
        path = Path(filename)
        if not path.exists():
            missing.append(filename)
        elif path.stat().st_size == 0:
            empty.append(filename)

    print(f"Expected generated files: {len(DOCUMENTS)}")
    print(f"Missing files: {len(missing)}")
    print(f"Empty files: {len(empty)}")

    for filename in missing:
        print(f"  MISSING {filename}")
    for filename in empty:
        print(f"  EMPTY   {filename}")

    if missing or empty:
        print("\nVALIDATION FAILED")
        return 1

    print("\nVALIDATION PASSED")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Phase 0.3 API/Data/Integration documentation."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing non-empty generated files.",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate without writing files.",
    )
    args = parser.parse_args()

    if not args.validate_only:
        result = write_documents(force=args.force)
        if result:
            return result

    return validate()


if __name__ == "__main__":
    sys.exit(main())
