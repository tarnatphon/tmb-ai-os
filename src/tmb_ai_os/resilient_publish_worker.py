from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from .audit_models import ContentAuditEvent, PublishQueueItem
from .publish_queue_service import PublishQueueService
from .publish_worker import (
    ProcessedPublish,
    PublishQueueWorker,
)
from .publishing import Publisher
from .retry_policy import RetryPolicy


@dataclass(frozen=True)
class QueueProcessSummary:
    processed: tuple[ProcessedPublish, ...]
    failed_queue_ids: tuple[int, ...]


class ResilientPublishQueueWorker:
    def __init__(
        self,
        publisher: Publisher,
        retry_policy: RetryPolicy | None = None,
    ) -> None:
        self.publisher = publisher
        self.retry_policy = retry_policy or RetryPolicy()

    def process_due(
        self,
        session: Session,
        *,
        limit: int = 20,
    ) -> QueueProcessSummary:
        queue_service = PublishQueueService()
        items = queue_service.list_due(session, limit=limit)

        processed: list[ProcessedPublish] = []
        failed_ids: list[int] = []

        for item in items:
            try:
                processed.append(
                    PublishQueueWorker(self.publisher).process_item(
                        session,
                        item.id,
                    )
                )
            except Exception as exc:
                self._handle_failure(session, item, str(exc))
                failed_ids.append(item.id)

        return QueueProcessSummary(
            processed=tuple(processed),
            failed_queue_ids=tuple(failed_ids),
        )

    def _handle_failure(
        self,
        session: Session,
        item: PublishQueueItem,
        message: str,
    ) -> None:
        attempt_count = getattr(item, "attempt_count", 0) + 1
        item.attempt_count = attempt_count
        item.last_error = message

        if self.retry_policy.can_retry(attempt_count):
            item.status = "retrying"
            item.scheduled_for = self.retry_policy.next_retry_at(attempt_count)
        else:
            item.status = "failed"
            item.scheduled_for = None

        session.add(
            ContentAuditEvent(
                content_id=item.content_id,
                event_type=item.status,
                actor=self.publisher.name,
                note=message,
                created_at=datetime.now(UTC),
            )
        )
        session.commit()
