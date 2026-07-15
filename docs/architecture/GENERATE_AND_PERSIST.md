# Generate-and-Persist Workflow

The canonical workflow now connects:

```text
Markdown Brief
    -> Knowledge Retrieval
    -> Multi-channel Generation
    -> Deterministic Prompt Hash
    -> Content History Repository
    -> Status API
```

API:

```text
POST /v5/content/preview
POST /v5/content/generate
GET  /v5/content/{content_id}/status
```
