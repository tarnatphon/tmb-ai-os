---
title: Engineering Handbook
version: 0.1.0
status: draft
owner: TMB AI OS Engineering
last_updated: 2026-07-27
---

# Engineering Handbook

## Core standards

All production changes must be:

- Reviewable
- Testable
- Secure
- Observable
- Documented
- Backward-compatible where practical
- Independent of a single AI or cloud vendor

## Definition of Done

A change is complete only when applicable checks pass:

1. Formatting and linting
2. Static type checking
3. Unit tests
4. Integration tests
5. Security checks
6. Documentation validation
7. Architecture validation
8. Build verification
9. Release notes
10. Rollback consideration

## Git workflow

- `main` must remain releasable.
- Work is performed on focused branches.
- Changes enter `main` through pull requests.
- Commit messages follow Conventional Commits.
- Large architectural changes require an ADR.
- Major business or governance decisions require an EDR.

## Commit examples

```text
feat(ai-gateway): add provider fallback routing
fix(auth): prevent expired token reuse
docs(architecture): define Company Brain boundaries
test(workflow): add approval transition coverage
Engineering principles

* Prefer clear boundaries over hidden coupling.
* Keep provider-specific code behind adapters.
* Do not bypass authorization or audit controls.
* Avoid premature distributed-system complexity.
* Add observability with production features.
* Automate repeatable validation.
    EOF

cat > docs/adr/ADR-0001-monorepo.md <<‘EOF’

title: ADR-0001 Monorepo Strategy
version: 0.1.0
status: accepted
owner: TMB AI OS Architecture Team
last_updated: 2026-07-27
decision_date: 2026-07-27

ADR-0001: Use a Monorepo

Context

TMB AI OS will contain applications, platform engines, shared packages,
developer tools, infrastructure, tests, and documentation that must evolve
under consistent standards.

Decision

Use a monorepo as the primary repository strategy.

Reasons

* Shared contracts can be versioned together.
* CI/CD and engineering standards remain consistent.
* Cross-module changes can be reviewed atomically.
* Documentation can evolve alongside source code.
* Dependency and compatibility validation is simpler during the foundation
    stage.

Consequences

Positive

* Easier code sharing
* Unified tooling
* Consistent releases and quality gates
* Better visibility across platform boundaries

Negative

* Repository size will grow.
* CI pipelines require path-aware optimization.
* Module ownership must be defined clearly.

Guardrails

* Enforce explicit package and domain boundaries.
* Prevent unrestricted cross-module imports.
* Use path-based CI execution where appropriate.
* Reassess repository strategy when scale provides evidence that separation is
    beneficial.
    EOF

cat > docs/edr/EDR-0001-project-charter.md <<‘EOF’

title: EDR-0001 Project Charter
version: 0.1.0
status: accepted
owner: TMB AI OS Steering Team
last_updated: 2026-07-27
decision_date: 2026-07-27

EDR-0001: TMB AI OS Project Charter

Decision

Develop TMB AI OS as an Enterprise Intelligence Platform rather than as a
single-purpose AI application.

Business objective

The first deployment must create practical value for Thai Modern Bags while
the platform architecture remains reusable by other organizations and
industries.

Phase 0 scope

Phase 0 establishes:

* Architecture and engineering governance
* Documentation standards
* Repository and CI/CD foundations
* Identity and access foundations
* AI Gateway foundations
* Company Brain foundations
* Plugin runtime foundations
* Web and desktop client foundations

Guiding principles

1. Business value before novelty
2. Human authority over consequential decisions
3. Security and privacy by design
4. AI-provider independence
5. Modular architecture
6. Explainability and auditability
7. Cross-platform access
8. Cloud, local, on-premises, and hybrid readiness
9. Open integration standards
10. Long-term maintainability

Out of scope for Phase 0

* Rebuilding a full ERP
* Supporting every enterprise module
* Autonomous high-impact decisions without approval
* Premature multi-region infrastructure
* A public marketplace launch

Success criteria

Phase 0 succeeds when the repository is reproducible, documented, testable, and
ready to support the first production-grade platform capabilities.
