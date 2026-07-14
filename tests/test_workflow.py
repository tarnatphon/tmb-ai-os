from datetime import UTC, datetime

import pytest

from tmb_ai_os.workflow import (
    InvalidWorkflowTransition,
    WorkflowRecord,
    WorkflowService,
    WorkflowStatus,
)


def test_valid_workflow_transition() -> None:
    record = WorkflowRecord(
        content_id="content-1",
        status=WorkflowStatus.DRAFT,
        updated_at=datetime.now(UTC),
    )

    updated = WorkflowService().transition(
        record,
        WorkflowStatus.GENERATED,
    )

    assert updated.status is WorkflowStatus.GENERATED


def test_invalid_workflow_transition() -> None:
    record = WorkflowRecord(
        content_id="content-1",
        status=WorkflowStatus.DRAFT,
        updated_at=datetime.now(UTC),
    )

    with pytest.raises(InvalidWorkflowTransition):
        WorkflowService().transition(
            record,
            WorkflowStatus.PUBLISHED,
        )
