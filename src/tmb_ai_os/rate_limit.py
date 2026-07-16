from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from threading import Lock


@dataclass(frozen=True)
class RateLimitDecision:
    allowed: bool
    remaining: int
    reset_at: datetime


class InMemoryRateLimiter:
    def __init__(
        self,
        *,
        max_requests: int,
        window_seconds: int,
    ) -> None:
        if max_requests < 1:
            raise ValueError("max_requests must be at least 1")
        if window_seconds < 1:
            raise ValueError("window_seconds must be at least 1")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._events: dict[str, deque[datetime]] = defaultdict(deque)
        self._lock = Lock()

    def check(
        self,
        key: str,
        *,
        now: datetime | None = None,
    ) -> RateLimitDecision:
        current = now or datetime.now(UTC)
        cutoff = current - timedelta(seconds=self.window_seconds)

        with self._lock:
            events = self._events[key]
            while events and events[0] <= cutoff:
                events.popleft()

            if len(events) >= self.max_requests:
                reset_at = events[0] + timedelta(seconds=self.window_seconds)
                return RateLimitDecision(
                    allowed=False,
                    remaining=0,
                    reset_at=reset_at,
                )

            events.append(current)
            remaining = self.max_requests - len(events)
            reset_at = events[0] + timedelta(seconds=self.window_seconds)
            return RateLimitDecision(
                allowed=True,
                remaining=remaining,
                reset_at=reset_at,
            )
