from sqlalchemy.orm import Session

from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.security import Role


def test_create_authenticate_and_revoke_api_key() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    service = ApiKeyService()
    created = service.create(
        session,
        key_id="admin-test",
        role=Role.ADMIN,
    )

    principal = service.authenticate(
        session,
        created.plaintext_key,
    )
    assert principal is not None
    assert principal.api_key_id == "admin-test"

    service.revoke(session, "admin-test")
    assert (
        service.authenticate(
            session,
            created.plaintext_key,
        )
        is None
    )

    session.close()
