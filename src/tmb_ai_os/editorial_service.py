from sqlalchemy import select
from sqlalchemy.orm import Session

from .audit_models import ContentAuditEvent, PublishQueueItem
from .editorial import (
    EditorialStatus,
    InvalidEditorialTransition,
    build_transition,
)
from .models import ContentRun


class EditorialContentNotFoundError(LookupError):
    pass


class EditorialService:
    def transition(
        self,
        session: Session,
        *,
        content_id: int,
        target: EditorialStatus,
        actor: str,
        note: str | None = None,
    ) -> ContentRun:
        row = session.get(ContentRun, content_id)
        if row is None:
            raise EditorialContentNotFoundError(f"Content run not found: {content_id}")

        try:
            current = EditorialStatus(row.status)
        except ValueError as exc:
            raise InvalidEditorialTransition(f"Unknown editorial status: {row.status}") from exc

        transition = build_transition(
            content_id=content_id,
            current=current,
            target=target,
            actor=actor,
            note=note,
        )

        row.status = target.value
        session.add(
            ContentAuditEvent(
                content_id=content_id,
                event_type=target.value,
                actor=actor,
                note=note,
                created_at=transition.occurred_at,
            )
        )

        if target is EditorialStatus.QUEUED:
            existing = session.scalar(
                select(PublishQueueItem).where(PublishQueueItem.content_id == content_id)
            )
            if existing is None:
                session.add(
                    PublishQueueItem(
                        content_id=content_id,
                        status=EditorialStatus.QUEUED.value,
                    )
                )

        session.commit()
        session.refresh(row)
        return row

    def list_queue(
        self,
        session: Session,
    ) -> list[PublishQueueItem]:
        return list(
            session.scalars(
                select(PublishQueueItem).order_by(PublishQueueItem.created_at.asc())
            ).all()
        )

    def list_audit(
        self,
        session: Session,
        *,
        content_id: int,
    ) -> list[ContentAuditEvent]:
        return list(
            session.scalars(
                select(ContentAuditEvent)
                .where(ContentAuditEvent.content_id == content_id)
                .order_by(ContentAuditEvent.created_at.asc())
            ).all()
        )
