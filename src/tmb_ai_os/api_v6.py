from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .database import get_db
from .editorial import (
    EditorialStatus,
    InvalidEditorialTransition,
)
from .editorial_service import (
    EditorialContentNotFoundError,
    EditorialService,
)

router = APIRouter(prefix="/v6", tags=["Milestone 4.7"])
DbSession = Annotated[Session, Depends(get_db)]


class EditorialActionRequest(BaseModel):
    actor: str = Field(min_length=2, max_length=120)
    note: str | None = Field(default=None, max_length=2000)


def _transition(
    *,
    content_id: int,
    target: EditorialStatus,
    payload: EditorialActionRequest,
    db: Session,
) -> dict[str, object]:
    try:
        row = EditorialService().transition(
            db,
            content_id=content_id,
            target=target,
            actor=payload.actor,
            note=payload.note,
        )
        return {
            "content_id": row.id,
            "status": row.status,
        }
    except EditorialContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except InvalidEditorialTransition as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/content/{content_id}/review")
def review_content(
    content_id: int,
    payload: EditorialActionRequest,
    db: DbSession,
) -> dict[str, object]:
    return _transition(
        content_id=content_id,
        target=EditorialStatus.REVIEWED,
        payload=payload,
        db=db,
    )


@router.post("/content/{content_id}/approve")
def approve_content(
    content_id: int,
    payload: EditorialActionRequest,
    db: DbSession,
) -> dict[str, object]:
    return _transition(
        content_id=content_id,
        target=EditorialStatus.APPROVED,
        payload=payload,
        db=db,
    )


@router.post("/content/{content_id}/reject")
def reject_content(
    content_id: int,
    payload: EditorialActionRequest,
    db: DbSession,
) -> dict[str, object]:
    return _transition(
        content_id=content_id,
        target=EditorialStatus.REJECTED,
        payload=payload,
        db=db,
    )


@router.post("/content/{content_id}/publish")
def queue_content(
    content_id: int,
    payload: EditorialActionRequest,
    db: DbSession,
) -> dict[str, object]:
    return _transition(
        content_id=content_id,
        target=EditorialStatus.QUEUED,
        payload=payload,
        db=db,
    )


@router.get("/publish-queue")
def list_publish_queue(
    db: DbSession,
) -> list[dict[str, object]]:
    items = EditorialService().list_queue(db)
    return [
        {
            "id": item.id,
            "content_id": item.content_id,
            "status": item.status,
            "scheduled_for": item.scheduled_for,
            "created_at": item.created_at,
        }
        for item in items
    ]


@router.get("/content/{content_id}/audit")
def list_content_audit(
    content_id: int,
    db: DbSession,
) -> list[dict[str, object]]:
    items = EditorialService().list_audit(
        db,
        content_id=content_id,
    )
    return [
        {
            "id": item.id,
            "event_type": item.event_type,
            "actor": item.actor,
            "note": item.note,
            "created_at": item.created_at,
        }
        for item in items
    ]
