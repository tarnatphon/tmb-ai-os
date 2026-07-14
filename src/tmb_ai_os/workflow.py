from dataclasses import dataclass, replace
from datetime import UTC, datetime
from enum import StrEnum


class WorkflowStatus(StrEnum):
    DRAFT = "draft"
    GENERATED = "generated"
    REVIEWED = "reviewed"
    APPROVED = "approved"
    PUBLISHED = "published"
    REJECTED = "rejected"


ALLOWED_TRANSITIONS: dict[WorkflowStatus, set[WorkflowStatus]] = {
    WorkflowStatus.DRAFT: {WorkflowStatus.GENERATED},
    WorkflowStatus.GENERATED: {
        WorkflowStatus.REVIEWED,
        WorkflowStatus.REJECTED,
    },
    WorkflowStatus.REVIEWED: {
        WorkflowStatus.APPROVED,
        WorkflowStatus.REJECTED,
    },
    WorkflowStatus.APPROVED: {WorkflowStatus.PUBLISHED},
    WorkflowStatus.PUBLISHED: set(),
    WorkflowStatus.REJECTED: {WorkflowStatus.DRAFT},
}


@dataclass(frozen=True)
class WorkflowRecord:
    content_id: str
    status: WorkflowStatus
    updated_at: datetime
    reviewer: str | None = None
    note: str | None = None


class InvalidWorkflowTransition(ValueError):
    pass


class WorkflowService:
    def transition(
        self,
        record: WorkflowRecord,
        target: WorkflowStatus,
        reviewer: str | None = None,
        note: str | None = None,
    ) -> WorkflowRecord:
        allowed = ALLOWED_TRANSITIONS[record.status]
        if target not in allowed:
            raise InvalidWorkflowTransition(f"Cannot transition from {record.status} to {target}")

        return replace(
            record,
            status=target,
            updated_at=datetime.now(UTC),
            reviewer=reviewer,
            note=note,
        )
