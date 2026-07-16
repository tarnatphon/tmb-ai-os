# Alerts and Incident Tracking

Alert sources:

- Readiness failures
- Failed publish queue items
- Future backup verification failures
- Future maintenance failures

Default notifier:

```text
dry_run
```

API:

```text
POST /v16/alerts/evaluate
GET  /v16/incidents
POST /v16/incidents/{incident_id}/acknowledge
POST /v16/incidents/{incident_id}/resolve
```
