# Secure Admin Dashboard

Login:

```text
http://127.0.0.1:8000/admin/login
```

The dashboard requires an API key with the `admin` role.

Protected APIs:

```text
GET /v18/dashboard/summary
GET /v18/dashboard/incidents
GET /v18/dashboard/notifications
GET /v19/admin/session
POST /v19/admin/audit
```

The API key is stored only in browser session storage and is removed when the
browser session ends or the user logs out.
