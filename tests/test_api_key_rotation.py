from sqlalchemy.orm import Session

from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.security import Role


def test_api_key_rotation_invalidates_old_key() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    service = ApiKeyService()
    created = service.create(
        session,
        key_id="rotate-test",
        role=Role.ADMIN,
    )
    rotated = service.rotate(session, "rotate-test")

    assert (
        service.authenticate(
            session,
            created.plaintext_key,
        )
        is None
    )
    assert (
        service.authenticate(
            session,
            rotated.plaintext_key,
        )
        is not None
    )

    session.close()
