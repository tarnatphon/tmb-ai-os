from sqlalchemy.orm import Session

from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.workflow_status import ContentStatusService


def test_status_service_returns_stored_status() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    stored = ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "content"},
        ),
    )

    status = ContentStatusService(ContentHistoryRepository()).get_status(session, stored.id)

    assert status.status == "generated"
    session.close()
