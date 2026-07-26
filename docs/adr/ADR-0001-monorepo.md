---
title: ADR-0001 Monorepo Strategy
version: 0.1.0
status: accepted
owner: TMB AI OS Architecture Team
last_updated: 2026-07-27
decision_date: 2026-07-27
---

# ADR-0001: Use a Monorepo

## Context

TMB AI OS contains applications, platform engines, shared packages, developer
tools, infrastructure, tests, plugins, SDKs, and documentation.

These components must evolve under consistent engineering standards while
maintaining clear architectural boundaries.

## Decision

TMB AI OS will use a monorepo as its primary repository strategy.

## Reasons

- Shared contracts can be versioned together.
- Cross-module changes can be reviewed atomically.
- CI/CD standards remain consistent.
- Documentation evolves alongside source code.
- Shared packages and SDKs can be reused safely.
- Dependency compatibility can be validated centrally.

## Alternatives considered

### Multiple repositories

Each service or application could use a separate repository.

This provides strong physical separation but increases release coordination,
dependency management, and governance complexity during the foundation stage.

### Hybrid repository model

Core components could remain in a monorepo while selected services use separate
repositories.

This remains a future option when scale, ownership, or security requirements
justify separation.

## Consequences

### Positive

- Unified tooling and quality gates
- Easier code reuse
- Consistent dependency management
- Atomic cross-platform changes
- Centralized architecture validation
- Simplified onboarding

### Negative

- Repository size will increase.
- CI pipelines must become path-aware.
- Module boundaries require automated enforcement.
- Ownership rules must remain explicit.

## Guardrails

- Every package must have a defined owner.
- Cross-domain imports must use approved public interfaces.
- Internal implementation details must not be imported across boundaries.
- CI jobs should run only for affected paths where practical.
- Architecture validation must detect prohibited dependencies.
- Large modules may be separated later through a new ADR.

## Review criteria

This decision should be reviewed when one or more of the following occurs:

- Repository performance materially affects developers.
- Independent release cycles become operationally necessary.
- Security requires physical repository isolation.
- Team ownership becomes difficult to manage.
- CI duration exceeds agreed service-level targets.

## Status

Accepted for Phase 0.
