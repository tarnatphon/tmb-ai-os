# TMB AI OS — Milestone 4.5: Content Persistence & API Migration

Canonical modules:
- `tmb_ai_os.content_records`
- `tmb_ai_os.content_history`
- `tmb_ai_os.api_v4`

Apply:

```bash
python scripts/apply_milestone_4_5.py
```

Validate:

```bash
ruff format .
ruff check .
mypy src
pytest
```

API:
- `POST /v4/content`
- `GET /v4/content`
- `GET /v4/content/{content_id}`
