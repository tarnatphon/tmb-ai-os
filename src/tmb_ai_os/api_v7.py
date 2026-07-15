from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .publish_worker import (
    PublishQueueItemNotFoundError,
    PublishQueueStateError,
    PublishQueueWorker,
)
from .publisher_factory import (
    PublisherName,
    UnsupportedPublisherError,
    create_publisher,
)

router = APIRouter(prefix="/v7", tags=["Milestone 4.8"])
DbSession = Annotated[Session, Depends(get_db)]


class ProcessQueueRequest(BaseModel):
    publisher: PublisherName = PublisherName.DRY_RUN
    queue_id: int | None = None


@router.get("/publishers")
def list_publishers() -> dict[str, list[str]]:
    return {"items": [publisher.value for publisher in PublisherName]}


@router.post("/publish-queue/process")
def process_publish_queue(
    payload: ProcessQueueRequest,
    db: DbSession,
) -> dict[str, object]:
    try:
        worker = PublishQueueWorker(create_publisher(payload.publisher))
        processed = (
            worker.process_item(db, payload.queue_id)
            if payload.queue_id is not None
            else worker.process_next(db)
        )

        if processed is None:
            return {
                "processed": False,
                "message": "No queued content available",
            }

        return {
            "processed": True,
            "queue_id": processed.queue_id,
            "content_id": processed.content_id,
            "provider": processed.result.provider,
            "external_id": processed.result.external_id,
            "published_at": processed.result.published_at,
            "metadata": processed.result.metadata,
        }
    except PublishQueueItemNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except PublishQueueStateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except UnsupportedPublisherError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/publish-queue/{queue_id}")
def get_publish_queue_item(
    queue_id: int,
    db: DbSession,
) -> dict[str, object]:
    from .audit_models import PublishQueueItem

    item = db.get(PublishQueueItem, queue_id)
    if item is None:
        raise HTTPException(
            status_code=404,
            detail=f"Publish queue item not found: {queue_id}",
        )

    return {
        "id": item.id,
        "content_id": item.content_id,
        "status": item.status,
        "scheduled_for": item.scheduled_for,
        "created_at": item.created_at,
    }
