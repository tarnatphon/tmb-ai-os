---
title: Webhook Security
phase: "0.3"
status: approved
owner: security
last_updated: 2026-07-30
tags: [webhooks, security, signatures, replay-protection]
---

# Webhook Security

## Scope

These requirements apply to inbound and outbound webhooks.

## Transport

Webhook endpoints require HTTPS with modern TLS. Redirects are disabled unless explicitly required and validated.

## Authentication

Inbound webhooks must verify a cryptographic signature or an equivalent provider-supported authentication mechanism.

Preferred design:

- HMAC using SHA-256 or stronger
- signature calculated over the exact raw request body
- timestamp included in the signed material
- key identifier included where rotation is supported

Never trust source IP alone as the primary control.

## Replay Protection

Reject requests whose signed timestamp falls outside the allowed window. Store a delivery identifier, event identifier, or signature digest to detect duplicates.

Duplicate delivery should return a safe success response after confirming that the original event was accepted.

## Payload Handling

- Read the raw body before parsing.
- Enforce body-size limits.
- Validate content type.
- Validate schema and event type.
- Reject unknown or malformed payloads.
- Do not log secrets or complete sensitive payloads.
- Preserve a correlation identifier.

## Processing

A webhook endpoint should authenticate, validate, enqueue durable work, and respond quickly. Long-running business operations must not execute directly in the request handler.

Consumers must be idempotent.

## Secrets and Rotation

Signing secrets are stored in approved secret management. Rotation supports a defined overlap period with both current and previous keys where required.

Exposed or suspected secrets are revoked immediately and investigated.

## Outbound Webhooks

Outbound webhook destinations must be validated and protected against SSRF. Block private, loopback, link-local, metadata-service, and disallowed network ranges unless explicitly approved.

Outbound deliveries must include:

- event identifier
- event type
- timestamp
- contract version
- signature
- retry-safe semantics

## Retry Policy

Retry only transient failures. Use bounded exponential backoff with jitter. Permanent failures must enter a visible failure state or dead-letter process.

## Audit

Record delivery metadata, verification outcome, processing state, retry count, and final result. Audit records must avoid storing unnecessary sensitive content.
