from sqlalchemy.orm import Session

from tmb_ai_os.audit_models import PublishQueueItem
from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.editorial import EditorialStatus
from tmb_ai_os.editorial_service import EditorialService
from tmb_ai_os.publish_worker import (
    PublishQueueStateError,
    PublishQueueWorker,
)
from tmb_ai_os.publishing import DryRunPublisher


def make_session() -> Session:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_worker_publishes_queued_content() -> None:
    session = make_session()
    stored = ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "content"},
        ),
    )

    editorial = EditorialService()
    editorial.transition(
        session,
        content_id=stored.id,
        target=EditorialStatus.REVIEWED,
        actor="reviewer",
    )
    editorial.transition(
        session,
        content_id=stored.id,
        target=EditorialStatus.APPROVED,
        actor="manager",
    )
    editorial.transition(
        session,
        content_id=stored.id,
        target=EditorialStatus.QUEUED,
        actor="publisher",
    )

    item = session.query(PublishQueueItem).one()
    processed = PublishQueueWorker(DryRunPublisher()).process_item(session, item.id)

    assert processed.content_id == stored.id
    assert item.status == "published"
    session.close()


def test_worker_rejects_published_item() -> None:
    session = make_session()
    stored = ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "content"},
        ),
    )
    item = PublishQueueItem(
        content_id=stored.id,
        status="published",
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    try:
        PublishQueueWorker(DryRunPublisher()).process_item(session, item.id)
    except PublishQueueStateError:
        pass
    else:
        raise AssertionError("Expected PublishQueueStateError")
    finally:
        session.close()
