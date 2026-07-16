from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True)
class RetentionPolicy:
    content_days: int = 365
    audit_days: int = 180
    backup_days: int = 90

    def __post_init__(self) -> None:
        for field_name, value in (
            ("content_days", self.content_days),
            ("audit_days", self.audit_days),
            ("backup_days", self.backup_days),
        ):
            if value < 1:
                raise ValueError(f"{field_name} must be at least 1")

    def content_cutoff(
        self,
        *,
        now: datetime | None = None,
    ) -> datetime:
        current = now or datetime.now(UTC)
        return current - timedelta(days=self.content_days)

    def audit_cutoff(
        self,
        *,
        now: datetime | None = None,
    ) -> datetime:
        current = now or datetime.now(UTC)
        return current - timedelta(days=self.audit_days)

    def backup_cutoff(
        self,
        *,
        now: datetime | None = None,
    ) -> datetime:
        current = now or datetime.now(UTC)
        return current - timedelta(days=self.backup_days)
