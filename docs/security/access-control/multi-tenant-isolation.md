---
title: Multi-Tenant Isolation
version: 0.1.0
status: draft
owner: TMB AI OS Security Team
last_updated: 2026-07-30
---

# Multi-Tenant Isolation

TMB AI OS must prevent data and permission leakage between organizations.

## Isolation requirements

- Every tenant-owned resource must include an organization identifier.
- Every tenant-aware query must include organization scope.
- Cross-organization access is denied by default.
- Cache keys must include tenant context.
- Search and vector indexes must preserve tenant boundaries.
- Files and object-storage paths must be tenant-scoped.
- Events must include tenant context.
- Audit records must retain organization attribution.

## Database controls

Application-level controls are mandatory.

Database-level protections, including row-level security, should be used where appropriate as defense in depth.

## Testing requirements

Automated tests must attempt:

- Cross-tenant reads
- Cross-tenant writes
- Identifier substitution
- Cache leakage
- Search-index leakage
- File-path traversal
- Background-job tenant confusion

Any cross-tenant data exposure is a critical security defect.
