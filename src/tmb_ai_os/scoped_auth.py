from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .api_key_scope_service import ApiKeyScopeService
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
        scopes = ApiKeyScopeService().get_scopes(
            db,
            principal.api_key_id,
        )
        if required_scope not in scopes:
            raise HTTPException(
                status_code=403,
                detail=(f"Missing required scope: {required_scope.value}"),
            )
        return principal

    return dependency
