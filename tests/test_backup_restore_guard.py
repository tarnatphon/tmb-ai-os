from pathlib import Path

import pytest

from tmb_ai_os.backups import BackupError, BackupManager


def test_restore_requires_confirmation(tmp_path: Path) -> None:
    manager = BackupManager(
        backup_dir=tmp_path / "backups",
        database_path=tmp_path / "database.db",
        content_dir=tmp_path / "content",
        knowledge_dir=tmp_path / "knowledge",
    )

    with pytest.raises(BackupError):
        manager.restore("missing", confirm=False)
