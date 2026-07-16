from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .dashboard_service import DashboardService
from .database import get_db
from .scoped_auth import scope_dependency
from .scopes import ApiScope
from .security import Principal

router = APIRouter(prefix="/v18", tags=["Milestone 5.9"])
DbSession = Annotated[Session, Depends(get_db)]
AdminPrincipal = Annotated[
    Principal,
    Depends(scope_dependency(ApiScope.DASHBOARD_READ)),
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
