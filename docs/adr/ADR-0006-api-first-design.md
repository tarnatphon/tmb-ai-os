---
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
