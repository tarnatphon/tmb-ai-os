from sqlalchemy.orm import Session

from .alerts import AlertSeverity, make_alert
from .health import build_readiness_report
from .incident_service import IncidentService
from .notifiers import Notifier
from .operations_metrics import get_publish_queue_metrics


class AlertEvaluator:
    def __init__(
        self,
        *,
        notifier: Notifier,
    ) -> None:
        self.notifier = notifier

    def evaluate(
        self,
        session: Session,
    ) -> list[int]:
        alerts = []

        readiness = build_readiness_report(session)
        if not readiness.ready:
            alerts.append(
                make_alert(
                    code="health.not_ready",
                    title="Application is not ready",
                    detail="One or more readiness checks failed",
                    severity=AlertSeverity.CRITICAL,
                )
            )

        queue = get_publish_queue_metrics(session)
        if queue.failed > 0:
            alerts.append(
                make_alert(
                    code="publish.failed_items",
                    title="Publish queue has failed items",
                    detail=f"Failed queue items: {queue.failed}",
                    severity=AlertSeverity.WARNING,
                )
            )

        incidents: list[int] = []
        service = IncidentService()
        for alert in alerts:
            incident = service.create_from_alert(
                session,
                alert=alert,
                notifier=self.notifier,
            )
            incidents.append(incident.id)

        return incidents
