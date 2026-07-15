from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from tmb_ai_os.audit_models import PublishQueueItem
from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.publish_queue_service import PublishQueueService


def make_session() -> Session:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_list_due_excludes_future_items() -> None:
    session = make_session()
    stored = ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "content"},
        ),
    )

    future_item = PublishQueueItem(
        content_id=stored.id,
        status="queued",
        scheduled_for=datetime.now(UTC) + timedelta(hours=1),
    )
    session.add(future_item)
    session.commit()

    assert PublishQueueService().list_due(session) == []
    session.close()
