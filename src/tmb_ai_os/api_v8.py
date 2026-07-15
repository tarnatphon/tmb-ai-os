from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .publish_queue_service import (
    PublishQueueNotFoundError,
    PublishQueueScheduleError,
    PublishQueueService,
)
from .publisher_factory import (
    PublisherName,
    create_publisher,
)
from .resilient_publish_worker import (
    ResilientPublishQueueWorker,
)

router = APIRouter(prefix="/v8", tags=["Milestone 4.9"])
DbSession = Annotated[Session, Depends(get_db)]


class ScheduleRequest(BaseModel):
    scheduled_for: datetime


class ProcessDueRequest(BaseModel):
    publisher: PublisherName = PublisherName.DRY_RUN
    limit: int = 20


@router.post("/publish-queue/{queue_id}/schedule")
def schedule_publish_queue_item(
    queue_id: int,
    payload: ScheduleRequest,
    db: DbSession,
) -> dict[str, object]:
    try:
        item = PublishQueueService().schedule(
            db,
            queue_id=queue_id,
            scheduled_for=payload.scheduled_for,
        )
        return {
            "id": item.id,
            "content_id": item.content_id,
            "status": item.status,
            "scheduled_for": item.scheduled_for,
        }
    except PublishQueueNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PublishQueueScheduleError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/publish-queue/process-due")
def process_due_publish_queue(
    payload: ProcessDueRequest,
    db: DbSession,
) -> dict[str, object]:
    summary = ResilientPublishQueueWorker(create_publisher(payload.publisher)).process_due(
        db,
        limit=payload.limit,
    )

    return {
        "processed_count": len(summary.processed),
        "failed_count": len(summary.failed_queue_ids),
        "processed": [
            {
                "queue_id": item.queue_id,
                "content_id": item.content_id,
                "external_id": item.result.external_id,
            }
            for item in summary.processed
        ],
        "failed_queue_ids": list(summary.failed_queue_ids),
    }


@router.get("/publish-queue/failed")
def list_failed_publish_queue(
    db: DbSession,
    limit: int = Query(default=100, ge=1, le=100),
) -> list[dict[str, object]]:
    items = PublishQueueService().list_failed(
        db,
        limit=limit,
    )

    return [
        {
            "id": item.id,
            "content_id": item.content_id,
            "status": item.status,
            "attempt_count": item.attempt_count,
            "last_error": item.last_error,
            "scheduled_for": item.scheduled_for,
        }
        for item in items
    ]
