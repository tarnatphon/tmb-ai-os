# Security Hardening

Milestone 5.2 adds:

- Request IDs
- Structured access logs
- Security response headers
- In-memory rate limiting
- Secret configuration validation

Environment:

```env
TMB_RATE_LIMIT_REQUESTS=60
TMB_RATE_LIMIT_WINDOW_SECONDS=60
TMB_REQUIRE_SECURE_API_KEY=true
```
