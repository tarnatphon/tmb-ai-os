# Scoped API Keys

Available scopes:

```text
dashboard:read
content:read
content:write
publish:run
incident:manage
security:admin
```

Keys inherit default scopes from their role until explicit scopes are assigned.

API:

```text
GET /v22/scopes
GET /v22/api-keys/{key_id}/scopes
PUT /v22/api-keys/{key_id}/scopes
```
