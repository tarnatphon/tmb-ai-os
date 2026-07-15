from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .audit_models import PublishQueueItem


class PublishQueueNotFoundError(LookupError):
    pass


class PublishQueueScheduleError(ValueError):
    pass


class PublishQueueService:
    def schedule(
        self,
        session: Session,
        *,
        queue_id: int,
        scheduled_for: datetime,
    ) -> PublishQueueItem:
        item = session.get(PublishQueueItem, queue_id)
        if item is None:
            raise PublishQueueNotFoundError(f"Publish queue item not found: {queue_id}")

        if item.status not in {"queued", "retrying"}:
            raise PublishQueueScheduleError(
                f"Queue item cannot be scheduled from status: {item.status}"
            )

        if scheduled_for.tzinfo is None:
            raise PublishQueueScheduleError("scheduled_for must include timezone information")

        item.scheduled_for = scheduled_for.astimezone(UTC)
        session.commit()
        session.refresh(item)
        return item

    def list_due(
        self,
        session: Session,
        *,
        now: datetime | None = None,
        limit: int = 20,
    ) -> list[PublishQueueItem]:
        current = now or datetime.now(UTC)
        safe_limit = min(max(limit, 1), 100)

        rows = session.scalars(
            select(PublishQueueItem)
            .where(PublishQueueItem.status.in_(["queued", "retrying"]))
            .where(
                (PublishQueueItem.scheduled_for.is_(None))
                | (PublishQueueItem.scheduled_for <= current)
            )
            .order_by(PublishQueueItem.created_at.asc())
            .limit(safe_limit)
        ).all()

        return list(rows)

    def list_failed(
        self,
        session: Session,
        *,
        limit: int = 100,
    ) -> list[PublishQueueItem]:
        safe_limit = min(max(limit, 1), 100)

        rows = session.scalars(
            select(PublishQueueItem)
            .where(PublishQueueItem.status == "failed")
            .order_by(PublishQueueItem.created_at.desc())
            .limit(safe_limit)
        ).all()

        return list(rows)
