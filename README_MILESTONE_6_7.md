# TMB AI OS — Milestone 6.7: API Key Usage Telemetry

Adds API key usage events, anomaly detection, risk summaries,
administrative endpoints, tests, and CI validation.

## Apply

```bash
python scripts/apply_milestone_6_7.py
```

## Validate

```bash
ruff format .
ruff check .
mypy src
pytest
python scripts/check_api_key_telemetry.py
```
