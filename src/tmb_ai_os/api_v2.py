from pathlib import Path

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from .config import get_settings
from .content import ContentRepository
from .knowledge import KeywordKnowledgeRetriever, KnowledgeRepository
from .multichannel import MultiChannelContentService
from .prompt_sdk import PromptBuilder
from .providers import GeminiGenerator

router = APIRouter(prefix="/v2", tags=["Milestone 2"])


class ContentFileRequest(BaseModel):
    path: str


def _knowledge_repository() -> KnowledgeRepository:
    return KnowledgeRepository(Path("knowledge"))


def _service(with_generator: bool) -> MultiChannelContentService:
    settings = get_settings()
    knowledge_repository = _knowledge_repository()
    generator = GeminiGenerator(settings) if with_generator else None

    return MultiChannelContentService(
        content_repository=ContentRepository(settings.content_dir),
        retriever=KeywordKnowledgeRetriever(knowledge_repository),
        prompt_builder=PromptBuilder(),
        generator=generator,
    )


@router.get("/knowledge")
def list_knowledge() -> dict[str, list[dict[str, object]]]:
    documents = _knowledge_repository().list_documents()
    return {
        "items": [
            {
                "path": str(document.path),
                "title": document.title,
                "category": document.category,
                "tags": list(document.tags),
            }
            for document in documents
        ]
    }


@router.get("/knowledge/search")
def search_knowledge(
    q: str = Query(min_length=2),
    limit: int = Query(default=4, ge=1, le=20),
) -> dict[str, list[dict[str, object]]]:
    retriever = KeywordKnowledgeRetriever(_knowledge_repository())
    results = retriever.search(q, limit=limit)
    return {
        "items": [
            {
                "title": result.document.title,
                "category": result.document.category,
                "score": result.score,
                "body": result.document.body,
            }
            for result in results
        ]
    }


@router.post("/content/preview")
def preview_content(payload: ContentFileRequest) -> dict[str, object]:
    try:
        outputs = _service(with_generator=False).preview(Path(payload.path))
        return {
            "items": [
                {
                    "channel": output.channel.value,
                    "prompt": output.prompt,
                }
                for output in outputs
            ]
        }
    except (FileNotFoundError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/content/generate")
def generate_content(payload: ContentFileRequest) -> dict[str, object]:
    try:
        outputs = _service(with_generator=True).generate(Path(payload.path))
        return {
            "items": [
                {
                    "channel": output.channel.value,
                    "text": output.text,
                }
                for output in outputs
            ]
        }
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
