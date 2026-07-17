from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .api_key_lifecycle import ApiKeyLifecycleService
from .database import get_db
from .scoped_auth import scope_dependency
from .scopes import ApiScope
from .security import Principal

router = APIRouter(prefix="/v25", tags=["Milestone 6.6"])
DbSession = Annotated[Session, Depends(get_db)]
SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(scope_dependency(ApiScope.SECURITY_ADMIN)),
]


class ConfigureLifecycleRequest(BaseModel):
    api_key_id: str
    expires_at: datetime | None = None
    rotation_required: bool = False


@router.post("/security/api-key-lifecycle")
def configure_lifecycle(
    payload: ConfigureLifecycleRequest,
    _: SecurityAdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    record = ApiKeyLifecycleService().configure(
        db,
        api_key_id=payload.api_key_id,
        expires_at=payload.expires_at,
        rotation_required=payload.rotation_required,
    )
    return {
        "api_key_id": record.api_key_id,
        "expires_at": record.expires_at,
        "rotation_required": record.rotation_required,
        "revoked_at": record.revoked_at,
    }


@router.post("/security/api-key-lifecycle/{api_key_id}/revoke")
def revoke_key(
    api_key_id: str,
    _: SecurityAdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    record = ApiKeyLifecycleService().revoke(
        db,
        api_key_id=api_key_id,
    )
    return {
        "api_key_id": record.api_key_id,
        "revoked_at": record.revoked_at,
    }


@router.get("/security/api-key-lifecycle/expiring")
def list_expiring_keys(
    _: SecurityAdminPrincipal,
    db: DbSession,
    days: int = Query(default=30, ge=0, le=365),
) -> list[dict[str, object]]:
    return [
        {
            "api_key_id": row.api_key_id,
            "expires_at": row.expires_at,
            "rotation_required": row.rotation_required,
        }
        for row in ApiKeyLifecycleService().expiring_within(
            db,
            days=days,
        )
    ]
