from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .admin_security import validate_admin_principal
from .database import get_db
from .security import Permission, Principal
from .security_service import SecurityAuditService
from .unified_auth import unified_permission_dependency

router = APIRouter(prefix="/v19", tags=["Milestone 6.0"])
DbSession = Annotated[Session, Depends(get_db)]
AdminPrincipal = Annotated[
    Principal,
    Depends(unified_permission_dependency(Permission.SECURITY_ADMIN)),
]


class AdminAuditRequest(BaseModel):
    action: str
    detail: str | None = None


@router.get("/admin/session")
def admin_session(
    principal: AdminPrincipal,
) -> dict[str, object]:
    return asdict(validate_admin_principal(principal))


@router.post("/admin/audit")
def admin_audit(
    payload: AdminAuditRequest,
    principal: AdminPrincipal,
    db: DbSession,
) -> dict[str, object]:
    event = SecurityAuditService().record(
        db,
        principal=principal,
        action=payload.action,
        outcome="success",
        detail=payload.detail,
    )

    return {
        "id": event.id,
        "action": event.action,
        "created_at": event.created_at,
    }
