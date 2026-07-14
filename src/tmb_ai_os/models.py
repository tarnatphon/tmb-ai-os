from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ContentRun(Base):
    __tablename__ = "content_runs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )
    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    pillar: Mapped[str] = mapped_column(
        String(120),
        default="General",
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="generated",
        nullable=False,
        index=True,
    )
    payload_json: Mapped[str] = mapped_column(
        Text,
        default="{}",
        nullable=False,
    )
    prompt_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        unique=True,
        index=True,
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at,
            "topic": self.topic,
            "pillar": self.pillar,
            "status": self.status,
            "payload_json": self.payload_json,
            "prompt_hash": self.prompt_hash,
        }
