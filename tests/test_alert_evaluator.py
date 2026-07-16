from sqlalchemy.orm import Session

from tmb_ai_os.alert_evaluator import AlertEvaluator
from tmb_ai_os.audit_models import PublishQueueItem
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.notifiers import DryRunNotifier


def test_alert_evaluator_creates_incident_for_failed_queue() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    session.add(
        PublishQueueItem(
            content_id=1,
            status="failed",
        )
    )
    session.commit()

    incident_ids = AlertEvaluator(notifier=DryRunNotifier()).evaluate(session)

    assert incident_ids
    session.close()
