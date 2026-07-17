# API Key Lifecycle

Lifecycle controls include:

- Optional expiration timestamp
- Forced rotation
- Revocation
- Expiring-key report
- Authentication enforcement dependency

API:

```text
POST /v25/security/api-key-lifecycle
POST /v25/security/api-key-lifecycle/{api_key_id}/revoke
GET  /v25/security/api-key-lifecycle/expiring
```
