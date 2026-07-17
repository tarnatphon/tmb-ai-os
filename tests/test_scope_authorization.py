import pytest
from sqlalchemy.orm import Session

from tmb_ai_os.api_key_scope_service import ApiKeyScopeService
from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.scope_authorization import (
    ScopeAuthorizationError,
    authorize_scope,
)
from tmb_ai_os.scopes import ApiScope
from tmb_ai_os.security import Role


def test_scope_authorization_rejects_missing_scope() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    created = ApiKeyService().create(
        session,
        key_id="scope-auth-test",
        role=Role.VIEWER,
    )
    principal = ApiKeyService().authenticate(
        session,
        created.plaintext_key,
    )
    assert principal is not None

    ApiKeyScopeService().replace_scopes(
        session,
        key_id="scope-auth-test",
        scopes={ApiScope.CONTENT_READ},
    )

    with pytest.raises(ScopeAuthorizationError):
        authorize_scope(
            session,
            principal=principal,
            required_scope=ApiScope.PUBLISH_RUN,
        )

    session.close()
