---
title: ADR-0005 Policy-Based Authorization
version: 0.1.0
status: accepted
owner: TMB AI OS Architecture Team
last_updated: 2026-07-30
decision_date: 2026-07-30
---

# ADR-0005: Adopt Policy-Based Authorization

## Context

Simple role checks are insufficient for a multi-tenant platform containing users, services, plugins, AI agents, confidential resources, and high-impact workflows.

## Decision

TMB AI OS will use centralized policy-based authorization with role-based and attribute-based inputs.

Authorization is deny by default.

## Consequences

### Positive

- Consistent enforcement
- Fine-grained permissions
- Better tenant isolation
- Support for contextual and risk-based controls
- Testable authorization behavior

### Negative

- Policy design and maintenance require governance.
- Authorization evaluation adds implementation complexity.
- Incorrect policies may deny valid work or grant excessive access.

## Guardrails

- User-interface controls must not be treated as authorization.
- Every protected resource requires server-side enforcement.
- Plugins and agents receive explicitly scoped permissions.
- Policy changes require automated tests.
- Denied and privileged operations must be auditable.
