# Contributing to TMB AI OS

## Development workflow

1. Create a branch from `develop`.
2. Use a focused branch name such as `feature/provider-openai` or `fix/gemini-retry`.
3. Add or update tests for every behavior change.
4. Run `make check` before committing.
5. Open a pull request into `develop`; releases merge from `develop` into `main`.

## Commit convention

Use Conventional Commits:

- `feat(scope): description`
- `fix(scope): description`
- `refactor(scope): description`
- `docs(scope): description`
- `test(scope): description`
- `chore(scope): description`

Examples:

```text
feat(provider): add Gemini model fallback
refactor(content): make Markdown the primary output
fix(api): preserve provider errors in HTTP responses
```

## Quality checks

```bash
make install-dev
make check
```

Never commit `.env`, API keys, generated databases, logs, virtual environments,
or customer-confidential documents.
