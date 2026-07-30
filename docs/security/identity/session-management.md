---
title: Session Management
version: 0.1.0
status: draft
owner: TMB AI OS Security Team
last_updated: 2026-07-30
---

# Session Management

Session management protects authenticated access after identity verification.

## Session principles

- Access tokens must be short-lived.
- Refresh credentials must be protected and rotatable.
- Sessions must be revocable.
- Session activity must be attributable to a user, client, and organization.
- Privileged actions may require recent authentication.

## Session metadata

A session should record:

- Session ID
- User ID
- Organization ID
- Client type
- Creation time
- Last activity time
- Expiration time
- Authentication strength
- Device information where permitted
- Revocation status

## Revocation triggers

Sessions may be revoked when:

- A user signs out.
- A password or passkey is changed.
- An administrator disables an account.
- A security incident is detected.
- Organization membership is removed.
- Privileges are materially changed.
- A refresh-token reuse event is detected.

## Storage requirements

- Browser session credentials must use secure cookie settings.
- Native applications must use operating-system secure storage.
- CLI credentials must use an approved local credential store.
- Refresh credentials must not be stored in plaintext.
