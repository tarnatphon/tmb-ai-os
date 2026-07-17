from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class AuthorizationEvent(Base):
    __tablename__ = "authorization_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    api_key_id: Mapped[str] = mapped_column(String(120), index=True)
    method: Mapped[str] = mapped_column(String(16), index=True)
    path: Mapped[str] = mapped_column(String(500), index=True)
    required_scope: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
        index=True,
    )
    decision: Mapped[str] = mapped_column(String(20), index=True)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        index=True,
    )
