from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .dashboard_service import DashboardService
from .database import get_db

router = APIRouter(prefix="/v18", tags=["Milestone 5.9"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/dashboard/summary")
def dashboard_summary(db: DbSession) -> dict[str, object]:
    return DashboardService().summary(db)


@router.get("/dashboard/incidents")
def dashboard_incidents(
    db: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, object]]:
    return DashboardService().incidents(db, limit=limit)


@router.get("/dashboard/notifications")
def dashboard_notifications(
    db: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[dict[str, object]]:
    return DashboardService().notifications(db, limit=limit)
