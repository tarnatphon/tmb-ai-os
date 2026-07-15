from dataclasses import dataclass
from datetime import UTC, datetime, timedelta


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 3
    base_delay_seconds: int = 60

    def next_retry_at(
        self,
        attempt_count: int,
        *,
        now: datetime | None = None,
    ) -> datetime:
        if attempt_count < 1:
            raise ValueError("attempt_count must be at least 1")

        current = now or datetime.now(UTC)
        delay = self.base_delay_seconds * (2 ** (attempt_count - 1))
        return current + timedelta(seconds=delay)

    def can_retry(self, attempt_count: int) -> bool:
        return attempt_count < self.max_attempts
