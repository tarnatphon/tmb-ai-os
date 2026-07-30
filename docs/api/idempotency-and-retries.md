---
title: Idempotency and Retries
version: 0.1.0
status: draft
owner: TMB AI OS API Team
last_updated: 2026-07-30
---

# Idempotency and Retries

Clients may retry requests safely.

## Idempotent Operations

GET

PUT

DELETE

PATCH (where applicable)

## POST Requests

POST requests that create resources should support an Idempotency-Key.

## Retry Strategy

Clients should retry only transient failures.

Recommended retryable responses:

429

502

503

504

## Rules

- Duplicate requests must not create duplicate resources.
- Idempotency keys expire after a defined period.
- Retry attempts must be logged.
- Background jobs should also be idempotent.
