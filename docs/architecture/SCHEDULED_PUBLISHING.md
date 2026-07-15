# Scheduled Publishing and Retry Policy

Queue states:

```text
queued
  -> published
  -> retrying
  -> failed
```

Retry delay uses exponential backoff:

```text
attempt 1: 60 seconds
attempt 2: 120 seconds
attempt 3: failed
```

API:

```text
POST /v8/publish-queue/{queue_id}/schedule
POST /v8/publish-queue/process-due
GET  /v8/publish-queue/failed
```
