# Backup and Restore

Create:
```bash
python scripts/create_backup.py
```

List:
```bash
python scripts/list_backups.py
```

Verify:
```bash
python scripts/verify_backup.py backup-YYYYMMDDTHHMMSSZ
```

Restore:
```bash
python scripts/restore_backup.py backup-YYYYMMDDTHHMMSSZ --confirm
```

Stop the application before restoring.
