from dataclasses import dataclass
from threading import Lock

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .audit_models import ContentAuditEvent, PublishQueueItem
from .models import ContentRun


@dataclass(frozen=True)
class PublishQueueMetrics:
    queued: int
    retrying: int
    failed: int
    published: int


@dataclass(frozen=True)
class ContentMetrics:
    total: int
    generated: int
    reviewed: int
    approved: int
    rejected: int
    queued: int
    published: int


@dataclass(frozen=True)
class AiMetrics:
    requests: int
    input_tokens: int
    output_tokens: int
    estimated_cost_usd: float


@dataclass(frozen=True)
class AgentMetrics:
    total_runs: int
    successful_runs: int
    failed_runs: int


@dataclass(frozen=True)
class WorkflowMetrics:
    total_runs: int
    active_runs: int
    failed_runs: int


@dataclass(frozen=True)
class OperationsMetrics:
    content: ContentMetrics
    publish_queue: PublishQueueMetrics
    audit_events: int
    ai: AiMetrics
    agents: AgentMetrics
    workflows: WorkflowMetrics


def _count_by_status(
    session: Session,
    model: type[ContentRun] | type[PublishQueueItem],
    status: str,
) -> int:
    value = session.scalar(select(func.count()).select_from(model).where(model.status == status))
    return int(value or 0)


def get_publish_queue_metrics(
    session: Session,
) -> PublishQueueMetrics:
    return PublishQueueMetrics(
        queued=_count_by_status(session, PublishQueueItem, "queued"),
        retrying=_count_by_status(session, PublishQueueItem, "retrying"),
        failed=_count_by_status(session, PublishQueueItem, "failed"),
        published=_count_by_status(session, PublishQueueItem, "published"),
    )


def get_content_metrics(
    session: Session,
) -> ContentMetrics:
    total_value = session.scalar(select(func.count()).select_from(ContentRun))
    return ContentMetrics(
        total=int(total_value or 0),
        generated=_count_by_status(session, ContentRun, "generated"),
        reviewed=_count_by_status(session, ContentRun, "reviewed"),
        approved=_count_by_status(session, ContentRun, "approved"),
        rejected=_count_by_status(session, ContentRun, "rejected"),
        queued=_count_by_status(session, ContentRun, "queued"),
        published=_count_by_status(session, ContentRun, "published"),
    )


def get_ai_metrics() -> AiMetrics:
    """Return the current AI usage metrics.

    Runtime persistence will be connected in a later Phase 7.2 change.
    """

    return AiMetrics(
        requests=0,
        input_tokens=0,
        output_tokens=0,
        estimated_cost_usd=0.0,
    )


_agent_metrics_lock = Lock()
_agent_total_runs = 0
_agent_successful_runs = 0
_agent_failed_runs = 0


def record_agent_run(*, approved: bool) -> None:
    """Record one completed AI agent orchestration run."""

    global _agent_total_runs
    global _agent_successful_runs
    global _agent_failed_runs

    with _agent_metrics_lock:
        _agent_total_runs += 1
        if approved:
            _agent_successful_runs += 1
        else:
            _agent_failed_runs += 1


def reset_agent_metrics() -> None:
    """Reset AI agent metrics for isolated tests."""

    global _agent_total_runs
    global _agent_successful_runs
    global _agent_failed_runs

    with _agent_metrics_lock:
        _agent_total_runs = 0
        _agent_successful_runs = 0
        _agent_failed_runs = 0


def get_agent_metrics() -> AgentMetrics:
    """Return a snapshot of the current AI agent execution metrics."""

    with _agent_metrics_lock:
        return AgentMetrics(
            total_runs=_agent_total_runs,
            successful_runs=_agent_successful_runs,
            failed_runs=_agent_failed_runs,
        )


def get_workflow_metrics() -> WorkflowMetrics:
    """Return the current workflow execution metrics."""

    return WorkflowMetrics(
        total_runs=0,
        active_runs=0,
        failed_runs=0,
    )


def get_operations_metrics(
    session: Session,
) -> OperationsMetrics:
    audit_value = session.scalar(select(func.count()).select_from(ContentAuditEvent))
    return OperationsMetrics(
        content=get_content_metrics(session),
        publish_queue=get_publish_queue_metrics(session),
        audit_events=int(audit_value or 0),
        ai=get_ai_metrics(),
        agents=get_agent_metrics(),
        workflows=get_workflow_metrics(),
    )
