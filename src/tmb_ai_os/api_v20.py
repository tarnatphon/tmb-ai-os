from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .api_key_service import ApiKeyNotFoundError, ApiKeyService
from .database import get_db
from .managed_security_dependencies import (
    managed_permission_dependency,
)
from .security import Permission, Principal, Role

router = APIRouter(prefix="/v20", tags=["Milestone 6.1"])
DbSession = Annotated[Session, Depends(get_db)]
AdminPrincipal = Annotated[
    Principal,
    Depends(managed_permission_dependency(Permission.SECURITY_ADMIN)),
]


class CreateApiKeyRequest(BaseModel):
    key_id: str = Field(min_length=3, max_length=120)
    role: Role
    expires_in_days: int | None = Field(
        default=None,
        ge=1,
        le=3650,
    )


@router.post("/api-keys")
def create_api_key(
    payload: CreateApiKeyRequest,
    _: AdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    try:
        created = ApiKeyService().create(
            db,
            key_id=payload.key_id,
            role=payload.role,
            expires_in_days=payload.expires_in_days,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    return {
        "key_id": created.key_id,
        "api_key": created.plaintext_key,
        "role": created.role,
        "expires_at": created.expires_at,
        "warning": "This key is shown only once",
    }


@router.get("/api-keys")
def list_api_keys(
    _: AdminPrincipal,
    db: DbSession,
) -> list[dict[str, object]]:
    return [
        {
            "key_id": row.key_id,
            "role": row.role,
            "active": row.active,
            "created_at": row.created_at,
            "expires_at": row.expires_at,
            "revoked_at": row.revoked_at,
        }
        for row in ApiKeyService().list(db)
    ]


@router.post("/api-keys/{key_id}/revoke")
def revoke_api_key(
    key_id: str,
    _: AdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    try:
        row = ApiKeyService().revoke(db, key_id)
    except ApiKeyNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "key_id": row.key_id,
        "active": row.active,
        "revoked_at": row.revoked_at,
    }


@router.post("/api-keys/{key_id}/rotate")
def rotate_api_key(
    key_id: str,
    _: AdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    try:
        created = ApiKeyService().rotate(db, key_id)
    except ApiKeyNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    return {
        "key_id": created.key_id,
        "api_key": created.plaintext_key,
        "role": created.role,
        "expires_at": created.expires_at,
        "warning": "This rotated key is shown only once",
    }
