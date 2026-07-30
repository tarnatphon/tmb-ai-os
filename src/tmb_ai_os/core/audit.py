from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class AuditRecord:
    action: str
    actor: str
    resource: str
    metadata: dict[str, Any] = field(default_factory=dict)
    record_id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


class AuditTrail:
    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self._records.append(record)

    def list_records(self) -> tuple[AuditRecord, ...]:
        return tuple(self._records)
