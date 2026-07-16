from dataclasses import dataclass
from enum import IntEnum

from sqlalchemy.orm import Session

from .alerts import AlertSeverity, make_alert
from .incident_models import Incident
from .incident_service import IncidentNotFoundError
from .notification_service import NotificationService
from .notifiers import Notifier


class EscalationLevel(IntEnum):
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3


@dataclass(frozen=True)
class EscalationResult:
    incident_id: int
    level: EscalationLevel
    delivery_id: int


class EscalationService:
    def escalate(
        self,
        session: Session,
        *,
        incident_id: int,
        level: EscalationLevel,
        notifier: Notifier,
    ) -> EscalationResult:
        incident = session.get(Incident, incident_id)
        if incident is None:
            raise IncidentNotFoundError(f"Incident not found: {incident_id}")

        severity = (
            AlertSeverity.CRITICAL if level >= EscalationLevel.LEVEL_2 else AlertSeverity.WARNING
        )
        alert = make_alert(
            code=f"incident.escalated.{incident.id}",
            title=f"Incident escalated to level {int(level)}",
            detail=incident.detail,
            severity=severity,
        )
        delivery = NotificationService().send(
            session,
            notifier=notifier,
            alert=alert,
        )
        return EscalationResult(
            incident_id=incident.id,
            level=level,
            delivery_id=delivery.id,
        )
