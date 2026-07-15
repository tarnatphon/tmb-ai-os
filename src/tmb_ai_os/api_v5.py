from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .config import get_settings
from .content import ContentRepository
from .content_history import (
    ContentHistoryRepository,
    ContentNotFoundError,
    DuplicatePromptError,
)
from .content_workflow import ContentWorkflowService
from .database import get_db
from .knowledge import (
    KeywordKnowledgeRetriever,
    KnowledgeRepository,
)
from .multichannel import MultiChannelContentService
from .prompt_sdk import PromptBuilder
from .provider_factory import create_text_generator
from .workflow_status import ContentStatusService

router = APIRouter(prefix="/v5", tags=["Milestone 4.6"])
DbSession = Annotated[Session, Depends(get_db)]


class WorkflowFileRequest(BaseModel):
    path: str


def _workflow_service(
    *,
    with_generator: bool,
) -> ContentWorkflowService:
    settings = get_settings()
    generator = create_text_generator(settings=settings) if with_generator else None

    multi_channel = MultiChannelContentService(
        content_repository=ContentRepository(settings.content_dir),
        retriever=KeywordKnowledgeRetriever(KnowledgeRepository(Path("knowledge"))),
        prompt_builder=PromptBuilder(),
        generator=generator,
    )

    return ContentWorkflowService(
        generator_service=multi_channel,
        history_repository=ContentHistoryRepository(),
    )


@router.post("/content/preview")
def preview_content(
    payload: WorkflowFileRequest,
) -> dict[str, object]:
    try:
        result = _workflow_service(with_generator=False).preview(Path(payload.path))
        return {
            "prompt_hash": result.prompt_hash,
            "items": [
                {
                    "channel": output.channel.value,
                    "prompt": output.prompt,
                }
                for output in result.outputs
            ],
        }
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.post("/content/generate")
def generate_content(
    payload: WorkflowFileRequest,
    db: DbSession,
) -> dict[str, object]:
    try:
        result = _workflow_service(with_generator=True).generate_and_store(
            db,
            Path(payload.path),
        )
        if result.stored is None:
            raise RuntimeError("Generated content was not persisted")

        return {
            "content_id": result.stored.id,
            "status": result.stored.status,
            "prompt_hash": result.prompt_hash,
            "channels": result.stored.channels,
        }
    except DuplicatePromptError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc
    except (
        FileNotFoundError,
        ValueError,
        RuntimeError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get("/content/{content_id}/status")
def get_content_status(
    content_id: int,
    db: DbSession,
) -> dict[str, object]:
    try:
        status = ContentStatusService(ContentHistoryRepository()).get_status(db, content_id)
        return {
            "content_id": status.content_id,
            "status": status.status,
            "updated_at": status.updated_at,
        }
    except ContentNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc
