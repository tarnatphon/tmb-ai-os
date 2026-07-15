# Approval Workflow and Publish Queue

Editorial flow:

```text
generated
  -> reviewed
  -> approved
  -> queued
  -> published
```

Rejection flow:

```text
generated -> rejected
reviewed  -> rejected
rejected  -> reviewed
```

API:

```text
POST /v6/content/{content_id}/review
POST /v6/content/{content_id}/approve
POST /v6/content/{content_id}/reject
POST /v6/content/{content_id}/publish
GET  /v6/publish-queue
GET  /v6/content/{content_id}/audit
```
