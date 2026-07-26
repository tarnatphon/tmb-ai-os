# Changelog


## Phase 7.2 — Workflow Runtime Metrics

Completed workflow-level operational metrics across runtime collection, API exposure, Prometheus rendering, and test isolation.

### Added

- workflow runtime metrics collector
- workflow success and failure tracking in `ContentWorkflowService`
- workflow metrics in `/v9/metrics/operations`
- Prometheus workflow counters and active-run gauge
- API and renderer regression tests
- automatic metrics reset between workflow tests

### Metrics

- `tmb_workflow_runs_total`
- `tmb_workflow_total_runs`
- `tmb_workflow_active_runs`
- `tmb_workflow_failed_runs_total`

### Validation

- 218 tests passed
- Ruff checks passed
- Ruff format validation passed
- mypy passed
- authentication migration validation passed

All notable changes follow Semantic Versioning and Conventional Commits.

## [2.0.0-dev.1] - 2026-07-14

### Added
- Content-first Markdown generation
- Gemini provider abstraction with model discovery, retry and fallback
- External prompt SDK
- Plain Markdown API endpoint
- SQLite draft history
- GitHub Actions quality pipeline
- Docker and macOS bootstrap workflows
- Repository governance, security, contribution and branching documentation
- Extension points for agents, workflows, knowledge and integrations

### Changed
- Removed large generated JSON packages as the canonical content artifact
- Separated vendor SDK logic from business services
