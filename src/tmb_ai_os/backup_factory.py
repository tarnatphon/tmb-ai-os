from pathlib import Path

from .backups import BackupManager
from .config import get_settings


def create_backup_manager() -> BackupManager:
    settings = get_settings()
    prefix = "sqlite:///"
    if not settings.database_url.startswith(prefix):
        raise ValueError("File backup currently supports SQLite only")

    return BackupManager(
        backup_dir=Path(settings.backup_dir),
        database_path=Path(settings.database_url.removeprefix(prefix)),
        content_dir=Path(settings.content_dir),
        knowledge_dir=Path("knowledge"),
    )
