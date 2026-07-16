from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .maintenance import MaintenanceConfirmationError
from .maintenance_factory import create_maintenance_service

router = APIRouter(prefix="/v15", tags=["Milestone 5.6"])
DbSession = Annotated[Session, Depends(get_db)]


class MaintenanceRunRequest(BaseModel):
    confirm: bool = False


@router.get("/maintenance/preview")
def maintenance_preview(
    db: DbSession,
) -> dict[str, object]:
    return asdict(create_maintenance_service().preview(db))


@router.post("/maintenance/run")
def run_maintenance(
    payload: MaintenanceRunRequest,
    db: DbSession,
) -> dict[str, object]:
    try:
        return asdict(
            create_maintenance_service().run(
                db,
                confirm=payload.confirm,
            )
        )
    except MaintenanceConfirmationError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.get("/maintenance/config")
def maintenance_config() -> dict[str, int]:
    settings = get_settings()
    return {
        "content_days": settings.retention_content_days,
        "audit_days": settings.retention_audit_days,
        "backup_days": settings.retention_backup_days,
    }
