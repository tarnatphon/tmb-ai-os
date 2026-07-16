from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy.orm import Session

from tmb_ai_os.backups import BackupManager
from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.maintenance import MaintenanceService
from tmb_ai_os.models import ContentRun
from tmb_ai_os.retention import RetentionPolicy


def test_maintenance_preview_counts_expired_content(
    tmp_path: Path,
) -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    stored = ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="Old content",
            channels={"facebook": "content"},
        ),
    )
    row = session.get(ContentRun, stored.id)
    assert row is not None
    row.created_at = datetime.now(UTC) - timedelta(days=400)
    session.commit()

    service = MaintenanceService(
        policy=RetentionPolicy(content_days=365),
        backup_manager=BackupManager(
            backup_dir=tmp_path / "backups",
            database_path=tmp_path / "database.db",
            content_dir=tmp_path / "content",
            knowledge_dir=tmp_path / "knowledge",
        ),
    )

    preview = service.preview(session)

    assert preview.content_rows == 1
    session.close()
