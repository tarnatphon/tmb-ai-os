from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .api_key_lifecycle import (
    ApiKeyLifecycleError,
    ApiKeyLifecycleService,
)
from .database import get_db
from .security import Permission, Principal
from .unified_auth import unified_permission_dependency

LifecyclePrincipal = Annotated[
    Principal,
    Depends(
        unified_permission_dependency(
            Permission.READ,
        )
    ),
]

DbSession = Annotated[Session, Depends(get_db)]


def lifecycle_principal_dependency(
    principal: LifecyclePrincipal,
    session: DbSession,
) -> Principal:
    try:
        ApiKeyLifecycleService().enforce(
            session,
            api_key_id=principal.api_key_id,
        )
    except ApiKeyLifecycleError as exc:
        raise HTTPException(
            status_code=401,
            detail=str(exc),
        ) from exc

    return principal
