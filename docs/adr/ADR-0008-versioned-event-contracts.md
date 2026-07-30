---
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
