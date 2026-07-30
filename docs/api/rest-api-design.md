---
title: REST API Design
version: 0.1.0
status: draft
owner: TMB AI OS API Team
last_updated: 2026-07-30
---

# REST API Design

TMB AI OS exposes versioned REST APIs for synchronous operations.

## Base URL

All public APIs must use:

/api/v1

## Design Principles

- Resource-oriented endpoints
- Predictable HTTP methods
- JSON request and response bodies
- Stable resource identifiers
- ISO 8601 timestamps
- Pagination for collections
- Correlation IDs for tracing
- OpenAPI-first development

## HTTP Methods

GET     Read resources

POST    Create resources or execute commands

PUT     Replace resources

PATCH   Partial updates

DELETE  Remove resources

## Naming

Good examples:

/organizations
/workflows
/workflows/{id}
/documents/{id}/versions

Avoid:

/getWorkflow
/createDocumentNow
/doAction

## Status Codes

200 OK

201 Created

202 Accepted

204 No Content

400 Bad Request

401 Unauthorized

403 Forbidden

404 Not Found

409 Conflict

422 Validation Failed

429 Too Many Requests

500 Internal Server Error

## Requirements

Every protected endpoint must:

- authenticate caller
- authorize access
- validate payload
- log request correlation id
- support audit logging
