---
title: Secrets Management
version: 0.1.0
status: draft
owner: TMB AI OS Security Team
last_updated: 2026-07-30
---

# Secrets Management

Secrets must be protected throughout development, testing, deployment, and operations.

## Secret examples

- API keys
- Database credentials
- OAuth client secrets
- Signing keys
- Encryption keys
- Webhook secrets
- Service-account credentials
- Deployment credentials

## Rules

- Secrets must never be committed to Git.
- Secrets must not appear in documentation examples.
- Production secrets must use an approved secret manager.
- Secrets must be scoped to the minimum required access.
- Secrets must support rotation.
- Secret access must be auditable.
- Development credentials must not be reused in production.
- Client-side applications must not contain server secrets.

## Local development

Local development may use ignored environment files.

A committed example file may contain variable names but must not contain working credentials.

## Rotation

Rotation procedures must define:

- Secret owner
- Rotation frequency
- Emergency rotation process
- Dependent systems
- Validation steps
- Rollback procedure
