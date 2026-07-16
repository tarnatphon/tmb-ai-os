# API Security and RBAC

Roles:

```text
viewer
reviewer
manager
publisher
admin
```

Header:

```text
X-API-Key: <configured key>
```

Environment:

```env
TMB_API_KEY=change-me
TMB_API_ROLE=admin
```

API:

```text
GET /v10/security/me
GET /v10/security/roles
GET /v10/security/audit
```
