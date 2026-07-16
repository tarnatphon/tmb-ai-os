# API Key Management

Bootstrap the first managed admin key:

```bash
python scripts/create_bootstrap_admin_key.py
```

The plaintext key is shown only once.

Managed keys are stored as SHA-256 hashes and support:

- Roles
- Expiration
- Revocation
- Rotation

API:

```text
POST /v20/api-keys
GET  /v20/api-keys
POST /v20/api-keys/{key_id}/revoke
POST /v20/api-keys/{key_id}/rotate
```
