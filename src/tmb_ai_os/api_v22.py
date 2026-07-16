from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .api_key_scope_service import ApiKeyScopeService
from .api_key_service import ApiKeyNotFoundError
from .database import get_db
from .scoped_auth import scope_dependency
from .scopes import ApiScope
from .security import Principal

router = APIRouter(prefix="/v22", tags=["Milestone 6.3"])
DbSession = Annotated[Session, Depends(get_db)]
SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(scope_dependency(ApiScope.SECURITY_ADMIN)),
]


class ReplaceScopesRequest(BaseModel):
    scopes: set[ApiScope]


@router.get("/scopes")
def list_available_scopes(
    _: SecurityAdminPrincipal,
) -> list[str]:
    return [scope.value for scope in ApiScope]


@router.get("/api-keys/{key_id}/scopes")
def get_api_key_scopes(
    key_id: str,
    _: SecurityAdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    try:
        scopes = ApiKeyScopeService().get_scopes(
            db,
            key_id,
        )
    except ApiKeyNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "key_id": key_id,
        "scopes": sorted(scope.value for scope in scopes),
    }


@router.put("/api-keys/{key_id}/scopes")
def replace_api_key_scopes(
    key_id: str,
    payload: ReplaceScopesRequest,
    _: SecurityAdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    try:
        scopes = ApiKeyScopeService().replace_scopes(
            db,
            key_id=key_id,
            scopes=payload.scopes,
        )
    except ApiKeyNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "key_id": key_id,
        "scopes": sorted(scope.value for scope in scopes),
    }
