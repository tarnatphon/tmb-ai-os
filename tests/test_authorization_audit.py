from sqlalchemy.orm import Session

from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.authorization_audit import AuthorizationAuditService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.scopes import ApiScope
from tmb_ai_os.security import Role


def test_authorization_event_is_recorded() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    created = ApiKeyService().create(
        session,
        key_id="audit-admin",
        role=Role.ADMIN,
    )
    principal = ApiKeyService().authenticate(
        session,
        created.plaintext_key,
    )
    assert principal is not None

    event = AuthorizationAuditService().record(
        session,
        principal=principal,
        method="GET",
        path="/v18/dashboard/summary",
        required_scope=ApiScope.DASHBOARD_READ,
        allowed=True,
    )

    assert event.decision == "allow"
    session.close()
