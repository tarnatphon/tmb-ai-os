from dataclasses import asdict

from fastapi import APIRouter, HTTPException

from .backup_factory import create_backup_manager
from .backups import BackupError

router = APIRouter(prefix="/v14", tags=["Milestone 5.5"])


@router.get("/backups")
def list_backups() -> list[dict[str, object]]:
    return [asdict(item) for item in create_backup_manager().list()]


@router.post("/backups/create")
def create_backup() -> dict[str, object]:
    try:
        return asdict(create_backup_manager().create())
    except (BackupError, OSError, ValueError) as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/backups/{backup_name}/verify")
def verify_backup(backup_name: str) -> dict[str, object]:
    try:
        return asdict(create_backup_manager().verify(backup_name))
    except BackupError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
