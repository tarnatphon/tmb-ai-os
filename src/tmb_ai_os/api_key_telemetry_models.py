from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ApiKeyUsageEvent(Base):
    __tablename__ = "api_key_usage_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    api_key_id: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )
    method: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        index=True,
    )
    status_code: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True,
    )
    client_ip: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
        index=True,
    )
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
        index=True,
    )
