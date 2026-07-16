from dataclasses import dataclass

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
class OperationsMetrics:
    content: ContentMetrics
    publish_queue: PublishQueueMetrics
    audit_events: int


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


def get_operations_metrics(
    session: Session,
) -> OperationsMetrics:
    audit_value = session.scalar(select(func.count()).select_from(ContentAuditEvent))
    return OperationsMetrics(
        content=get_content_metrics(session),
        publish_queue=get_publish_queue_metrics(session),
        audit_events=int(audit_value or 0),
    )
