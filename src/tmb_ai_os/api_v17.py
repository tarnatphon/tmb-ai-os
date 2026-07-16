from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .alerts import AlertSeverity, make_alert
from .database import get_db
from .escalation import EscalationLevel, EscalationService
from .incident_service import IncidentNotFoundError
from .notification_service import NotificationService
from .notifier_factory import (
    UnsupportedNotifierError,
    create_notifier,
)

router = APIRouter(prefix="/v17", tags=["Milestone 5.8"])
DbSession = Annotated[Session, Depends(get_db)]


class TestNotificationRequest(BaseModel):
    title: str = "TMB AI OS test notification"
    detail: str = "Notification channel test"


class EscalationRequest(BaseModel):
    level: EscalationLevel = EscalationLevel.LEVEL_1


@router.post("/notifications/test")
def test_notification(
    payload: TestNotificationRequest,
    db: DbSession,
) -> dict[str, object]:
    try:
        delivery = NotificationService().send(
            db,
            notifier=create_notifier(),
            alert=make_alert(
                code="notification.test",
                title=payload.title,
                detail=payload.detail,
                severity=AlertSeverity.INFO,
            ),
        )
        return {
            "delivery_id": delivery.id,
            "status": delivery.status,
            "provider": delivery.provider,
        }
    except UnsupportedNotifierError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/notifications/deliveries")
def list_notification_deliveries(
    db: DbSession,
    limit: int = Query(default=100, ge=1, le=100),
) -> list[dict[str, object]]:
    items = NotificationService().list_deliveries(
        db,
        limit=limit,
    )
    return [
        {
            "id": item.id,
            "provider": item.provider,
            "alert_code": item.alert_code,
            "status": item.status,
            "attempt_count": item.attempt_count,
            "response_code": item.response_code,
            "detail": item.detail,
            "created_at": item.created_at,
        }
        for item in items
    ]


@router.post("/incidents/{incident_id}/escalate")
def escalate_incident(
    incident_id: int,
    payload: EscalationRequest,
    db: DbSession,
) -> dict[str, object]:
    try:
        result = EscalationService().escalate(
            db,
            incident_id=incident_id,
            level=payload.level,
            notifier=create_notifier(),
        )
        return {
            "incident_id": result.incident_id,
            "level": int(result.level),
            "delivery_id": result.delivery_id,
        }
    except IncidentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
    except UnsupportedNotifierError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
