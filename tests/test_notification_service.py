from sqlalchemy.orm import Session

from tmb_ai_os.alerts import AlertSeverity, make_alert
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.notification_service import NotificationService
from tmb_ai_os.notifiers import DryRunNotifier


def test_notification_delivery_is_recorded() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    delivery = NotificationService().send(
        session,
        notifier=DryRunNotifier(),
        alert=make_alert(
            code="test.notification",
            title="Test",
            detail="Test detail",
            severity=AlertSeverity.INFO,
        ),
    )

    assert delivery.status == "delivered"
    assert delivery.provider == "dry_run"
    session.close()
