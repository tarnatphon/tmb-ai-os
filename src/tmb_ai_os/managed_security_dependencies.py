from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .api_key_service import ApiKeyService
from .database import get_db
from .security import Permission, Principal, require_permission

DbSession = Annotated[Session, Depends(get_db)]


def get_managed_principal(
    db: DbSession,
    x_api_key: Annotated[str | None, Header()] = None,
) -> Principal:
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key",
        )

    principal = ApiKeyService().authenticate(
        db,
        x_api_key,
    )
    if principal is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid, expired, or revoked API key",
        )

    return principal


def managed_permission_dependency(
    permission: Permission,
) -> Callable[[Principal], Principal]:
    def dependency(
        principal: Annotated[
            Principal,
            Depends(get_managed_principal),
        ],
    ) -> Principal:
        try:
            require_permission(principal, permission)
        except PermissionError as exc:
            raise HTTPException(
                status_code=403,
                detail=str(exc),
            ) from exc
        return principal

    return dependency
