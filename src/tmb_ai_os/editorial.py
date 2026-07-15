from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum


class EditorialStatus(StrEnum):
    GENERATED = "generated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    REJECTED = "rejected"
    QUEUED = "queued"
    PUBLISHED = "published"


ALLOWED_EDITORIAL_TRANSITIONS: dict[
    EditorialStatus,
    set[EditorialStatus],
] = {
    EditorialStatus.GENERATED: {
        EditorialStatus.REVIEWED,
        EditorialStatus.REJECTED,
    },
    EditorialStatus.REVIEWED: {
        EditorialStatus.APPROVED,
        EditorialStatus.REJECTED,
    },
    EditorialStatus.APPROVED: {
        EditorialStatus.QUEUED,
    },
    EditorialStatus.REJECTED: {
        EditorialStatus.REVIEWED,
    },
    EditorialStatus.QUEUED: {
        EditorialStatus.PUBLISHED,
    },
    EditorialStatus.PUBLISHED: set(),
}


class InvalidEditorialTransition(ValueError):
    pass


@dataclass(frozen=True)
class EditorialTransition:
    content_id: int
    from_status: EditorialStatus
    to_status: EditorialStatus
    actor: str
    note: str | None
    occurred_at: datetime


def validate_transition(
    current: EditorialStatus,
    target: EditorialStatus,
) -> None:
    if target not in ALLOWED_EDITORIAL_TRANSITIONS[current]:
        raise InvalidEditorialTransition(f"Cannot transition from {current} to {target}")


def build_transition(
    *,
    content_id: int,
    current: EditorialStatus,
    target: EditorialStatus,
    actor: str,
    note: str | None = None,
) -> EditorialTransition:
    validate_transition(current, target)
    return EditorialTransition(
        content_id=content_id,
        from_status=current,
        to_status=target,
        actor=actor,
        note=note,
        occurred_at=datetime.now(UTC),
    )
