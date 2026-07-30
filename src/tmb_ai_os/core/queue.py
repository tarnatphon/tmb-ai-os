from __future__ import annotations

import asyncio
import heapq
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID, uuid4

JobHandler = Callable[[dict[str, Any]], Awaitable[None]]


@dataclass(order=True, slots=True)
class Job:
    priority: int
    sequence: int
    name: str = field(compare=False)
    payload: dict[str, Any] = field(compare=False)
    max_retries: int = field(default=3, compare=False)
    attempts: int = field(default=0, compare=False)
    job_id: UUID = field(default_factory=uuid4, compare=False)


class JobQueue:
    def __init__(self) -> None:
        self._heap: list[Job] = []
        self._handlers: dict[str, JobHandler] = {}
        self._condition = asyncio.Condition()
        self._sequence = 0

    def register(self, name: str, handler: JobHandler) -> None:
        self._handlers[name] = handler

    async def enqueue(
        self,
        name: str,
        payload: dict[str, Any],
        *,
        priority: int = 100,
        max_retries: int = 3,
    ) -> UUID:
        async with self._condition:
            self._sequence += 1
            job = Job(priority, self._sequence, name, payload, max_retries)
            heapq.heappush(self._heap, job)
            self._condition.notify()
            return job.job_id

    async def process_one(self) -> Job:
        async with self._condition:
            if not self._heap:
                raise LookupError("Queue is empty")
            job = heapq.heappop(self._heap)

        handler = self._handlers.get(job.name)
        if handler is None:
            raise KeyError(f"No handler registered for job: {job.name}")

        try:
            job.attempts += 1
            await handler(job.payload)
        except Exception:
            if job.attempts < job.max_retries:
                async with self._condition:
                    heapq.heappush(self._heap, job)
                    self._condition.notify()
            raise
        return job

    @property
    def size(self) -> int:
        return len(self._heap)
