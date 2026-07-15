# Publisher Adapters and Queue Worker

Publishing flow:

```text
approved
  -> queued
  -> queue worker
  -> publisher adapter
  -> published
  -> audit event
```

Milestone 4.8 enables only the `dry_run` publisher.

Real platform adapters must be implemented behind the same `Publisher`
protocol and require explicit credentials and permissions.
