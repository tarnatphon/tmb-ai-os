from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class ManagedApiKeyScope(Base):
    __tablename__ = "managed_api_key_scopes"
    __table_args__ = (
        UniqueConstraint(
            "api_key_id",
            "scope",
            name="uq_managed_api_key_scope",
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    api_key_id: Mapped[int] = mapped_column(
        ForeignKey("managed_api_keys.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    scope: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        index=True,
    )
