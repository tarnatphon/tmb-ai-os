from sqlalchemy.orm import Session

from tmb_ai_os.audit_models import (
    ContentAuditEvent,
    PublishQueueItem,
)
from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.editorial import EditorialStatus
from tmb_ai_os.editorial_service import EditorialService


def make_session() -> Session:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_review_approve_and_queue_content() -> None:
    session = make_session()
    stored = ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "content"},
        ),
    )

    service = EditorialService()
    service.transition(
        session,
        content_id=stored.id,
        target=EditorialStatus.REVIEWED,
        actor="reviewer",
    )
    service.transition(
        session,
        content_id=stored.id,
        target=EditorialStatus.APPROVED,
        actor="manager",
    )
    row = service.transition(
        session,
        content_id=stored.id,
        target=EditorialStatus.QUEUED,
        actor="publisher",
    )

    assert row.status == "queued"
    assert len(service.list_queue(session)) == 1
    assert len(service.list_audit(session, content_id=stored.id)) == 3
    assert session.query(ContentAuditEvent).count() == 3
    assert session.query(PublishQueueItem).count() == 1
    session.close()
