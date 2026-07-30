---
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
