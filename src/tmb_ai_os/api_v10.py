from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .database import get_db
from .security import ROLE_PERMISSIONS, Permission, Principal, Role
from .security_dependencies import (
    get_principal,
    permission_dependency,
)
from .security_service import SecurityAuditService

router = APIRouter(prefix="/v10", tags=["Milestone 5.1"])
DbSession = Annotated[Session, Depends(get_db)]
AdminPrincipal = Annotated[
    Principal,
    Depends(permission_dependency(Permission.SECURITY_ADMIN)),
]


@router.get("/security/me")
def current_principal(
    principal: Annotated[Principal, Depends(get_principal)],
) -> dict[str, object]:
    return {
        "api_key_id": principal.api_key_id,
        "role": principal.role.value,
        "permissions": sorted(permission.value for permission in ROLE_PERMISSIONS[principal.role]),
    }


@router.get("/security/roles")
def list_roles(
    _: AdminPrincipal,
) -> dict[str, dict[str, list[str]]]:
    return {
        "roles": {
            role.value: sorted(permission.value for permission in ROLE_PERMISSIONS[role])
            for role in Role
        }
    }


@router.get("/security/audit")
def list_security_audit(
    _: AdminPrincipal,
    db: DbSession,
    limit: int = Query(default=100, ge=1, le=100),
) -> list[dict[str, object]]:
    events = SecurityAuditService().list_events(
        db,
        limit=limit,
    )
    return [
        {
            "id": event.id,
            "actor": event.actor,
            "role": event.role,
            "action": event.action,
            "outcome": event.outcome,
            "detail": event.detail,
            "created_at": event.created_at,
        }
        for event in events
    ]
