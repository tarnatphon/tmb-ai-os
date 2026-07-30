---
title: API Error Handling
version: 0.1.0
status: draft
owner: TMB AI OS API Team
last_updated: 2026-07-30
---

# API Error Handling

Errors must be predictable and machine-readable.

## Standard Error

{
  "error": {
    "code": "resource_not_found",
    "message": "Workflow was not found.",
    "request_id": "uuid",
    "details": {}
  }
}

## Principles

- Never leak internal stack traces.
- Messages should help API consumers.
- Error codes remain stable.
- Include request identifiers.
- Validation errors identify invalid fields.
- Security errors never reveal sensitive information.

## Categories

Validation

Authentication

Authorization

Business Rules

Concurrency

Rate Limiting

Infrastructure

Unknown Errors
