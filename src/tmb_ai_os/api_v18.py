from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .dashboard_service import DashboardService
from .database import get_db
from .security import Permission, Principal
from .unified_auth import unified_permission_dependency

router = APIRouter(prefix="/v18", tags=["Milestone 5.9"])
DbSession = Annotated[Session, Depends(get_db)]
AdminPrincipal = Annotated[
    Principal,
    Depends(unified_permission_dependency(Permission.OPERATIONS_READ)),
]


@router.get("/dashboard/summary")
def dashboard_summary(db: DbSession) -> dict[str, object]:
    return DashboardService().summary(db)


@router.get("/dashboard/incidents")
def dashboard_incidents(
    _: AdminPrincipal,
    db: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, object]]:
    return DashboardService().incidents(db, limit=limit)


@router.get("/dashboard/notifications")
def dashboard_notifications(
    _: AdminPrincipal,
    db: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, object]]:
    return DashboardService().notifications(db, limit=limit)
