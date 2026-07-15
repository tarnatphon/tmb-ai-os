import json
from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from .audit_models import ContentAuditEvent, PublishQueueItem
from .content_records import decode_channels
from .editorial import EditorialStatus
from .models import ContentRun
from .publishing import Publisher, PublishRequest, PublishResult


class PublishQueueItemNotFoundError(LookupError):
    pass


class PublishQueueStateError(ValueError):
    pass


@dataclass(frozen=True)
class ProcessedPublish:
    queue_id: int
    content_id: int
    result: PublishResult


class PublishQueueWorker:
    def __init__(self, publisher: Publisher) -> None:
        self.publisher = publisher

    def process_next(
        self,
        session: Session,
    ) -> ProcessedPublish | None:
        item = session.scalar(
            select(PublishQueueItem)
            .where(PublishQueueItem.status == EditorialStatus.QUEUED.value)
            .order_by(PublishQueueItem.created_at.asc())
            .limit(1)
        )
        if item is None:
            return None

        return self.process_item(session, item.id)

    def process_item(
        self,
        session: Session,
        queue_id: int,
    ) -> ProcessedPublish:
        item = session.get(PublishQueueItem, queue_id)
        if item is None:
            raise PublishQueueItemNotFoundError(f"Publish queue item not found: {queue_id}")

        if item.status == EditorialStatus.PUBLISHED.value:
            raise PublishQueueStateError(f"Queue item already published: {queue_id}")

        if item.status != EditorialStatus.QUEUED.value:
            raise PublishQueueStateError(f"Queue item is not ready: {queue_id}")

        content = session.get(ContentRun, item.content_id)
        if content is None:
            raise PublishQueueStateError(f"Content run not found: {item.content_id}")

        result = self.publisher.publish(
            PublishRequest(
                content_id=content.id,
                channels=decode_channels(content.payload_json),
            )
        )

        item.status = EditorialStatus.PUBLISHED.value
        content.status = EditorialStatus.PUBLISHED.value

        session.add(
            ContentAuditEvent(
                content_id=content.id,
                event_type=EditorialStatus.PUBLISHED.value,
                actor=self.publisher.name,
                note=json.dumps(
                    {
                        "provider": result.provider,
                        "external_id": result.external_id,
                        "metadata": result.metadata,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                ),
                created_at=result.published_at,
            )
        )
        session.commit()
        session.refresh(item)

        return ProcessedPublish(
            queue_id=item.id,
            content_id=content.id,
            result=result,
        )
