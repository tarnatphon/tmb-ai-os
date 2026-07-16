from sqlalchemy.orm import Session

from tmb_ai_os.api_key_scope_service import ApiKeyScopeService
from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.scopes import ApiScope
from tmb_ai_os.security import Role


def test_replace_and_get_api_key_scopes() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    ApiKeyService().create(
        session,
        key_id="scope-test",
        role=Role.VIEWER,
    )

    service = ApiKeyScopeService()
    replaced = service.replace_scopes(
        session,
        key_id="scope-test",
        scopes={
            ApiScope.DASHBOARD_READ,
            ApiScope.CONTENT_READ,
        },
    )

    assert ApiScope.DASHBOARD_READ in replaced
    assert (
        service.get_scopes(
            session,
            "scope-test",
        )
        == replaced
    )

    session.close()
