import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.content.engine import DuplicateContentError, generate_content
from app.core.database import SessionLocal
from app.core.models import ContentRun
from app.core.schemas import GenerateRequest
from app.providers.errors import ProviderError

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health")
def health():
    return {"status": "ok", "architecture": "content-first"}


@router.post("/content/generate")
def generate(payload: GenerateRequest, db: DbSession):
    try:
        return generate_content(db, payload)
    except DuplicateContentError as exc:
        raise HTTPException(409, str(exc)) from exc
    except ProviderError as exc:
        raise HTTPException(503, str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(500, f"Generation failed: {exc}") from exc


@router.post("/content/generate.md", response_class=PlainTextResponse)
def generate_markdown(payload: GenerateRequest, db: DbSession):
    return generate_content(db, payload).markdown


@router.get("/content")
def list_content(db: DbSession, limit: int = 20):
    safe_limit = min(max(limit, 1), 100)
    rows = db.query(ContentRun).order_by(ContentRun.created_at.desc()).limit(safe_limit).all()
    return [
        {
            "id": row.id,
            "created_at": row.created_at,
            "topic": row.topic,
            "pillar": row.pillar,
            "status": row.status,
            "content": json.loads(row.payload_json),
        }
        for row in rows
    ]
