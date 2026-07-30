---
title: Authorization Model
version: 0.1.0
status: draft
owner: TMB AI OS Security Team
last_updated: 2026-07-30
---

# Authorization Model

TMB AI OS uses centralized, policy-based authorization.

## Authorization inputs

Authorization decisions may consider:

- Subject identity
- Organization
- Workspace
- Role
- Permission
- Resource ownership
- Resource classification
- Requested action
- Authentication strength
- Environment
- Time
- Risk level

## Model

Role-based access control provides broad permission grouping.

Attribute-based and policy-based controls provide contextual restrictions.

## Decision pattern

Every protected request must produce one of these outcomes:

- Allow
- Deny
- Require additional authentication
- Require human approval

## Default behavior

Authorization is deny by default.

A request is allowed only when an explicit policy grants the requested action.

## Enforcement rules

- Enforcement must occur at service and resource boundaries.
- User-interface visibility is not an authorization control.
- Background workers must enforce the same policies as interactive clients.
- Plugins and agents must receive explicitly scoped permissions.
- Authorization failures must be auditable.
- Policies must support automated tests.
