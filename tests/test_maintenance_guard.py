from pathlib import Path

import pytest
from sqlalchemy.orm import Session

from tmb_ai_os.backups import BackupManager
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.maintenance import (
    MaintenanceConfirmationError,
    MaintenanceService,
)
from tmb_ai_os.retention import RetentionPolicy


def test_maintenance_requires_confirmation(
    tmp_path: Path,
) -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    service = MaintenanceService(
        policy=RetentionPolicy(),
        backup_manager=BackupManager(
            backup_dir=tmp_path / "backups",
            database_path=tmp_path / "database.db",
            content_dir=tmp_path / "content",
            knowledge_dir=tmp_path / "knowledge",
        ),
    )

    with pytest.raises(MaintenanceConfirmationError):
        service.run(session, confirm=False)

    session.close()
