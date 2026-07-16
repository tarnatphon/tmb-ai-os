from sqlalchemy.orm import Session

from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.security import Role


def test_managed_key_authentication() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    created = ApiKeyService().create(
        session,
        key_id="managed-admin",
        role=Role.ADMIN,
    )

    principal = ApiKeyService().authenticate(
        session,
        created.plaintext_key,
    )

    assert principal is not None
    assert principal.api_key_id == "managed-admin"
    session.close()
