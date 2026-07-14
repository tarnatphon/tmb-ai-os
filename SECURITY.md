# Security Policy

## Reporting a vulnerability

Do not open a public issue for security vulnerabilities. Report suspected issues
to the repository owner or the internal Thai Modern Bags technology contact.
Include reproduction steps, affected files, impact, and a proposed mitigation if known.

## Secrets

- Store secrets only in `.env` or the deployment secret manager.
- Never commit API keys, credentials, customer data, quotation data, or production exports.
- Rotate a secret immediately if it appears in Git history or logs.

## Supported branch

Security fixes are applied to the latest release on `main` and the active `develop` branch.
