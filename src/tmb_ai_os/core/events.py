from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

EventHandler = Callable[["Event"], Awaitable[None]]


@dataclass(frozen=True, slots=True)
class Event:
    name: str
    payload: dict[str, Any]
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, event_name: str, handler: EventHandler) -> None:
        async with self._lock:
            if handler not in self._handlers[event_name]:
                self._handlers[event_name].append(handler)

    async def publish(self, event: Event) -> None:
        handlers = tuple(self._handlers.get(event.name, ()))
        if handlers:
            await asyncio.gather(*(handler(event) for handler in handlers))

    def subscriber_count(self, event_name: str) -> int:
        return len(self._handlers.get(event_name, ()))
