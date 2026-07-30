---
title: Incident Response
version: 0.1.0
status: draft
owner: TMB AI OS Security Team
last_updated: 2026-07-30
---

# Incident Response

TMB AI OS requires a repeatable process for responding to security incidents.

## Incident stages

1. Detection
2. Triage
3. Containment
4. Eradication
5. Recovery
6. Communication
7. Post-incident review

## Severity levels

### Critical

Confirmed or highly probable major compromise, tenant-data exposure, credential theft, or destructive activity.

### High

Serious security impact with limited scope or strong containment.

### Medium

Security weakness or suspicious activity without confirmed major impact.

### Low

Minor security issue with limited risk.

## Immediate actions

Responders should:

- Preserve evidence.
- Record timestamps and actions.
- Revoke compromised credentials.
- Contain affected systems.
- Avoid destroying logs or forensic evidence.
- Notify the designated incident owner.
- Assess affected organizations and data.
- Document recovery decisions.

## Post-incident requirements

Every significant incident must produce:

- Root-cause analysis
- Impact assessment
- Timeline
- Corrective actions
- Regression tests
- Monitoring improvements
- Assigned owners and deadlines
