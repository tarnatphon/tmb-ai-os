from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import Session

from .content_history import ContentHistoryRepository


@dataclass(frozen=True)
class ContentStatus:
    content_id: int
    status: str
    updated_at: datetime


class ContentStatusService:
    def __init__(
        self,
        repository: ContentHistoryRepository,
    ) -> None:
        self.repository = repository

    def get_status(
        self,
        session: Session,
        content_id: int,
    ) -> ContentStatus:
        stored = self.repository.get(session, content_id)
        return ContentStatus(
            content_id=stored.id,
            status=stored.status,
            updated_at=stored.created_at,
        )
