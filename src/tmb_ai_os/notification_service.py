from sqlalchemy import select
from sqlalchemy.orm import Session

from .alerts import Alert
from .notification_models import NotificationDelivery
from .notifiers import Notifier


class NotificationService:
    def send(
        self,
        session: Session,
        *,
        notifier: Notifier,
        alert: Alert,
    ) -> NotificationDelivery:
        result = notifier.send(alert)

        delivery = NotificationDelivery(
            provider=result.provider,
            alert_code=alert.code,
            status="delivered" if result.delivered else "failed",
            attempt_count=1,
            response_code=self._response_code(result.detail),
            detail=result.detail,
        )
        session.add(delivery)
        session.commit()
        session.refresh(delivery)
        return delivery

    def list_deliveries(
        self,
        session: Session,
        *,
        limit: int = 100,
    ) -> list[NotificationDelivery]:
        safe_limit = min(max(limit, 1), 100)
        return list(
            session.scalars(
                select(NotificationDelivery)
                .order_by(NotificationDelivery.created_at.desc())
                .limit(safe_limit)
            ).all()
        )

    @staticmethod
    def _response_code(detail: str) -> int | None:
        if not detail.startswith("HTTP "):
            return None
        try:
            return int(detail.removeprefix("HTTP "))
        except ValueError:
            return None
