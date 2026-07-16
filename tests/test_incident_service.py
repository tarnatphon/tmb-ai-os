from sqlalchemy.orm import Session

from tmb_ai_os.alerts import AlertSeverity, make_alert
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.incident_service import IncidentService
from tmb_ai_os.notifiers import DryRunNotifier


def test_incident_lifecycle() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    incident = IncidentService().create_from_alert(
        session,
        alert=make_alert(
            code="test.alert",
            title="Test alert",
            detail="Test detail",
            severity=AlertSeverity.WARNING,
        ),
        notifier=DryRunNotifier(),
    )

    acknowledged = IncidentService().acknowledge(
        session,
        incident.id,
    )
    assert acknowledged.status == "acknowledged"

    resolved = IncidentService().resolve(
        session,
        incident.id,
    )
    assert resolved.status == "resolved"
    session.close()
