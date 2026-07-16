from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .alert_evaluator import AlertEvaluator
from .database import get_db
from .incident_service import (
    IncidentNotFoundError,
    IncidentService,
    InvalidIncidentStateError,
)
from .notifiers import DryRunNotifier

router = APIRouter(prefix="/v16", tags=["Milestone 5.7"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("/alerts/evaluate")
def evaluate_alerts(
    db: DbSession,
) -> dict[str, object]:
    incident_ids = AlertEvaluator(notifier=DryRunNotifier()).evaluate(db)

    return {
        "incident_ids": incident_ids,
        "count": len(incident_ids),
    }


@router.get("/incidents")
def list_incidents(
    db: DbSession,
    limit: int = Query(default=100, ge=1, le=100),
) -> list[dict[str, object]]:
    items = IncidentService().list_incidents(
        db,
        limit=limit,
    )
    return [
        {
            "id": item.id,
            "code": item.code,
            "title": item.title,
            "detail": item.detail,
            "severity": item.severity,
            "status": item.status,
            "created_at": item.created_at,
            "acknowledged_at": item.acknowledged_at,
            "resolved_at": item.resolved_at,
        }
        for item in items
    ]


@router.post("/incidents/{incident_id}/acknowledge")
def acknowledge_incident(
    incident_id: int,
    db: DbSession,
) -> dict[str, object]:
    try:
        item = IncidentService().acknowledge(
            db,
            incident_id,
        )
        return {
            "id": item.id,
            "status": item.status,
        }
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except InvalidIncidentStateError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.post("/incidents/{incident_id}/resolve")
def resolve_incident(
    incident_id: int,
    db: DbSession,
) -> dict[str, object]:
    try:
        item = IncidentService().resolve(
            db,
            incident_id,
        )
        return {
            "id": item.id,
            "status": item.status,
        }
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
