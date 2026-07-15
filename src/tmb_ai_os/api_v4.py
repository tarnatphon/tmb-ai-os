from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .content_history import (
    ContentHistoryRepository,
    ContentNotFoundError,
    DuplicatePromptError,
)
from .content_records import ContentCreate, ContentRead, StoredContent
from .database import get_db

router = APIRouter(prefix="/v4", tags=["Milestone 4.5"])
DbSession = Annotated[Session, Depends(get_db)]


def _to_read(content: StoredContent) -> ContentRead:
    return ContentRead(
        id=content.id,
        created_at=content.created_at,
        topic=content.topic,
        pillar=content.pillar,
        status=content.status,
        channels=content.channels,
        prompt_hash=content.prompt_hash,
    )


@router.post("/content", response_model=ContentRead, status_code=201)
def create_content(
    payload: ContentCreate,
    db: DbSession,
) -> ContentRead:
    repository = ContentHistoryRepository()
    try:
        return _to_read(repository.create(db, payload))
    except DuplicatePromptError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/content", response_model=list[ContentRead])
def list_content(
    db: DbSession,
    limit: int = Query(default=20, ge=1, le=100),
) -> list[ContentRead]:
    repository = ContentHistoryRepository()
    return [_to_read(item) for item in repository.list(db, limit=limit)]


@router.get("/content/{content_id}", response_model=ContentRead)
def get_content(
    content_id: int,
    db: DbSession,
) -> ContentRead:
    repository = ContentHistoryRepository()
    try:
        return _to_read(repository.get(db, content_id))
    except ContentNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
