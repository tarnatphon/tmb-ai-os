---
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
