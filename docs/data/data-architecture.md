---
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
