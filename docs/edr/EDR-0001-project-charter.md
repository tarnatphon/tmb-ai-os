---
title: EDR-0001 Project Charter
version: 0.1.0
status: accepted
owner: TMB AI OS Steering Team
last_updated: 2026-07-27
decision_date: 2026-07-27
---

# EDR-0001: TMB AI OS Project Charter

## Decision

TMB AI OS will be developed as an Enterprise Intelligence Platform rather than
as a single-purpose AI application.

## Mission

Build a trusted platform that helps organizations think, decide, execute,
learn, and continuously improve.

## Initial business objective

The first implementation must deliver measurable value to Thai Modern Bags
while preserving an architecture that can later support other organizations
and industries.

## Platform scope

TMB AI OS will provide a shared foundation for:

- Organizational identity and access control
- Company knowledge and memory
- Multi-provider AI access
- Workflow and automation
- Human approvals
- Plugin and integration capabilities
- Cross-platform user experiences
- Auditability and observability
- Developer APIs and SDKs

## Phase 0 scope

Phase 0 establishes:

- Architecture governance
- Engineering standards
- Documentation standards
- Repository structure
- CI/CD foundations
- Identity and access foundations
- AI Gateway foundations
- Company Brain foundations
- Plugin runtime foundations
- Web and desktop foundations
- Developer SDK foundations

## Guiding principles

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

## Out of scope for Phase 0

- Rebuilding a complete ERP
- Supporting every enterprise department
- Public marketplace launch
- Premature multi-region deployment
- Autonomous high-impact decisions without approval
- Building a proprietary foundation model
- Supporting every possible AI provider immediately

## Success criteria

Phase 0 succeeds when:

- The repository can be cloned and validated consistently.
- Documentation is version-controlled and cross-referenced.
- CI/CD quality gates pass reliably.
- Architecture decisions are recorded.
- Core modules have clearly defined boundaries.
- The first platform capabilities can be implemented without restructuring the
  entire repository.
- Security, authorization, logging, and testing are part of the foundation.

## Governance

Major architecture changes require an ADR.

Major business, product, policy, or governance decisions require an EDR.

Changes to this charter require review by the project steering team and must be
submitted through a pull request.

## Status

Accepted for Phase 0.
