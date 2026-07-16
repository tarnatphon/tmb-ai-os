from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from .config import get_settings
from .security import (
    AuthenticationError,
    Permission,
    Principal,
    Role,
    require_permission,
    verify_api_key,
)


def get_principal(
    x_api_key: Annotated[str | None, Header()] = None,
) -> Principal:
    settings = get_settings()

    if not verify_api_key(
        x_api_key or "",
        settings.api_key,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

    try:
        role = Role(settings.api_role)
    except ValueError as exc:
        raise AuthenticationError(f"Invalid configured API role: {settings.api_role}") from exc

    return Principal(
        api_key_id="primary",
        role=role,
    )


def permission_dependency(
    permission: Permission,
) -> Callable[[Principal], Principal]:
    def dependency(
        principal: Annotated[Principal, Depends(get_principal)],
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
