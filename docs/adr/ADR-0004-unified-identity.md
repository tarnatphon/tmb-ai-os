---
title: ADR-0004 Unified Identity Architecture
version: 0.1.0
status: accepted
owner: TMB AI OS Architecture Team
last_updated: 2026-07-30
decision_date: 2026-07-30
---

# ADR-0004: Adopt a Unified Identity Architecture

## Context

TMB AI OS contains multiple applications, services, plugins, agents, and automation components.

Independent authentication implementations would create inconsistent security controls and duplicate sensitive logic.

## Decision

TMB AI OS will use one unified identity boundary for authentication, session management, service identities, and identity-provider integration.

Applications and domain modules must not implement independent password verification or token issuance.

## Consequences

### Positive

- Consistent authentication policy
- Centralized auditability
- Easier session revocation
- Better enterprise SSO support
- Reduced duplicate security logic

### Negative

- Identity availability becomes platform-critical.
- Migration from legacy authentication requires controlled compatibility.
- Identity changes require careful review.

## Guardrails

- Access tokens must be short-lived.
- Refresh credentials must be rotatable and revocable.
- Service identities must use scoped permissions.
- Privileged actions may require stronger authentication.
- Authentication events must be auditable.
