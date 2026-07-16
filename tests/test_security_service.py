from sqlalchemy.orm import Session

from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.security import Principal, Role
from tmb_ai_os.security_service import SecurityAuditService


def test_security_audit_service_records_event() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    principal = Principal(
        api_key_id="primary",
        role=Role.ADMIN,
    )

    event = SecurityAuditService().record(
        session,
        principal=principal,
        action="security.test",
        outcome="success",
    )

    assert event.actor == "primary"
    assert len(SecurityAuditService().list_events(session)) == 1
    session.close()
