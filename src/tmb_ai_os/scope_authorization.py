from sqlalchemy.orm import Session

from .api_key_scope_service import ApiKeyScopeService
from .scopes import ApiScope
from .security import Principal


class ScopeAuthorizationError(PermissionError):
    pass


def authorize_scope(
    session: Session,
    *,
    principal: Principal,
    required_scope: ApiScope,
) -> None:
    scopes = ApiKeyScopeService().get_scopes(
        session,
        principal.api_key_id,
    )
    if required_scope not in scopes:
        raise ScopeAuthorizationError(f"Missing required scope: {required_scope.value}")
