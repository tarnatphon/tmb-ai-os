from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .api_key_service import ApiKeyService
from .config import get_settings
from .database import get_db
from .security import Permission, Principal, Role, require_permission

DbSession = Annotated[Session, Depends(get_db)]


def authenticate_request(
    db: DbSession,
    x_api_key: Annotated[str | None, Header()] = None,
) -> Principal:
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Missing API key",
        )

    managed = ApiKeyService().authenticate(db, x_api_key)
    if managed is not None:
        return managed

    settings = get_settings()
    if settings.legacy_api_key_fallback_enabled:
        if x_api_key == settings.api_key:
            return Principal(
                api_key_id="legacy-env",
                role=Role(settings.api_role),
            )

    raise HTTPException(
        status_code=401,
        detail="Invalid, expired, or revoked API key",
    )


def unified_permission_dependency(
    permission: Permission,
) -> Callable[[Principal], Principal]:
    def dependency(
        principal: Annotated[
            Principal,
            Depends(authenticate_request),
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
