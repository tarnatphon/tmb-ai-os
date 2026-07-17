from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .api_key_scope_service import ApiKeyScopeService
from .api_key_service import ApiKeyNotFoundError
from .database import get_db
from .scopes import ApiScope
from .security import Principal
from .unified_auth import authenticate_request

DbSession = Annotated[Session, Depends(get_db)]


def scope_dependency(
    required_scope: ApiScope,
) -> Callable[[Principal, Session], Principal]:
    def dependency(
        principal: Annotated[
            Principal,
            Depends(authenticate_request),
        ],
        db: DbSession,
    ) -> Principal:
        try:
            scopes = ApiKeyScopeService().get_scopes(
                db,
                principal.api_key_id,
            )
        except ApiKeyNotFoundError as exc:
            raise HTTPException(
                status_code=401,
                detail="API key is not registered for scoped access",
            ) from exc
        if required_scope not in scopes:
            raise HTTPException(
                status_code=403,
                detail=(f"Missing required scope: {required_scope.value}"),
            )
        return principal

    return dependency
