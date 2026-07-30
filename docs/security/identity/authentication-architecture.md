---
title: Authentication Architecture
version: 0.1.0
status: draft
owner: TMB AI OS Security Team
last_updated: 2026-07-30
---

# Authentication Architecture

TMB AI OS uses a unified authentication architecture for users, services, applications, plugins, and automation agents.

## Objectives

- Centralize identity verification.
- Support web, desktop, mobile, CLI, API, and service clients.
- Prevent individual modules from implementing independent authentication.
- Support enterprise identity providers.
- Maintain complete authentication audit records.

## Supported authentication methods

- Email and password
- Passkeys
- One-time verification codes
- OAuth 2.0 and OpenID Connect
- Enterprise single sign-on
- Service accounts
- Short-lived machine credentials

## Authentication flow

1. A client submits credentials to the identity boundary.
2. The identity service validates the authentication method.
3. The identity service evaluates account and organization status.
4. A short-lived access token is issued.
5. A refresh mechanism is issued only to eligible clients.
6. Security-relevant activity is recorded.

## Security requirements

- Passwords must use an approved adaptive password hash.
- Multi-factor authentication must be available.
- Privileged users should require stronger authentication.
- Authentication errors must not reveal whether an account exists.
- Login attempts must be rate-limited.
- Suspicious activity must generate security events.
- Tokens must be signed, scoped, and short-lived.
- Authentication secrets must never appear in logs.

## Trust boundaries

Applications must not verify passwords directly.

All authentication decisions must pass through the approved identity service or trusted identity-provider adapter.
