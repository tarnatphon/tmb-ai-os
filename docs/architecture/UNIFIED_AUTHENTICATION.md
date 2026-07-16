# Unified Authentication

Authentication order:

1. Managed database-backed API keys
2. Legacy environment API key fallback
3. Reject request

Disable the legacy fallback after all clients are migrated:

```env
TMB_LEGACY_API_KEY_FALLBACK_ENABLED=false
```

Validation endpoint:

```text
POST /v21/auth/validate
```
