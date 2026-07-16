from sqlalchemy.orm import Session

from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.escalation import EscalationLevel, EscalationService
from tmb_ai_os.incident_models import Incident
from tmb_ai_os.notifiers import DryRunNotifier


def test_incident_escalation_creates_delivery() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    incident = Incident(
        code="test.incident",
        title="Test incident",
        detail="Test detail",
        severity="warning",
        status="open",
    )
    session.add(incident)
    session.commit()
    session.refresh(incident)

    result = EscalationService().escalate(
        session,
        incident_id=incident.id,
        level=EscalationLevel.LEVEL_2,
        notifier=DryRunNotifier(),
    )

    assert result.delivery_id > 0
    session.close()
