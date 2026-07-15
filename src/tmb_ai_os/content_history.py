from sqlalchemy import select
from sqlalchemy.orm import Session

from .content_records import (
    ContentCreate,
    StoredContent,
    decode_channels,
    encode_channels,
)
from .models import ContentRun


class ContentNotFoundError(LookupError):
    pass


class DuplicatePromptError(ValueError):
    pass


class ContentHistoryRepository:
    def create(
        self,
        session: Session,
        payload: ContentCreate,
    ) -> StoredContent:
        if payload.prompt_hash is not None:
            existing = session.scalar(
                select(ContentRun).where(ContentRun.prompt_hash == payload.prompt_hash)
            )
            if existing is not None:
                raise DuplicatePromptError(f"Prompt already stored: {payload.prompt_hash}")

        row = ContentRun(
            topic=payload.topic,
            pillar=payload.pillar,
            status=payload.status,
            payload_json=encode_channels(payload.channels),
            prompt_hash=payload.prompt_hash,
        )
        session.add(row)
        session.commit()
        session.refresh(row)
        return self._to_stored(row)

    def list(
        self,
        session: Session,
        *,
        limit: int = 20,
    ) -> list[StoredContent]:
        safe_limit = min(max(limit, 1), 100)
        rows = session.scalars(
            select(ContentRun).order_by(ContentRun.created_at.desc()).limit(safe_limit)
        ).all()
        return [self._to_stored(row) for row in rows]

    def get(
        self,
        session: Session,
        content_id: int,
    ) -> StoredContent:
        row = session.get(ContentRun, content_id)
        if row is None:
            raise ContentNotFoundError(f"Content run not found: {content_id}")
        return self._to_stored(row)

    @staticmethod
    def _to_stored(row: ContentRun) -> StoredContent:
        return StoredContent(
            id=row.id,
            created_at=row.created_at,
            topic=row.topic,
            pillar=row.pillar,
            status=row.status,
            channels=decode_channels(row.payload_json),
            prompt_hash=row.prompt_hash,
        )
