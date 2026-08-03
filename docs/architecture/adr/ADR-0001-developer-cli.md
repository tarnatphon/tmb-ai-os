# ADR-0001: Developer CLI Architecture

## Status

Accepted

## Context

TMB AI OS requires repeatable developer commands for repository validation, module generation, testing, diagnostics, and releases.

Independent scripts would create multiple entry points, inconsistent interfaces, and additional maintenance overhead.

## Decision

The repository will provide one developer CLI entry point.

The target invocation is:

`python -m tools.tmb <command>`

Developer commands will be implemented as separate command modules behind this entry point.

The `scripts/` directory remains reserved for bootstrap, migration, CI, and operational helpers.

## Consequences

Benefits:

- Developers learn one command structure.
- Commands can share validation, logging, and error handling.
- Individual commands remain independently testable.
- The CLI can later be exposed as an installed console command.

Costs:

- Initial package structure is required.
- Existing standalone tooling must eventually migrate behind the CLI.

## Compatibility

This decision does not modify application runtime APIs.

Existing tooling remains available until equivalent CLI commands are implemented and validated.

## Follow-up

- Create the `tools.tmb` package.
- Add the repository validation command.
- Migrate module generation after validation coverage is available.
- Integrate the CLI with GitHub Actions only after local validation passes.
