# TMB AI OS — Milestone 5.5: Backup, Restore & Disaster Recovery

Features:
- SQLite backup
- Content and knowledge archive
- SHA-256 manifest verification
- Safe restore with confirmation
- API endpoints under `/v14`

Apply:
```bash
python scripts/apply_milestone_5_5.py
```

Validate:
```bash
ruff format .
ruff check .
mypy src
pytest
```
