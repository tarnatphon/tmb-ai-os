from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .alerts import Alert, IncidentStatus
from .incident_models import Incident
from .notifiers import Notifier


class IncidentNotFoundError(LookupError):
    pass


class InvalidIncidentStateError(ValueError):
    pass


class IncidentService:
    def create_from_alert(
        self,
        session: Session,
        *,
        alert: Alert,
        notifier: Notifier,
    ) -> Incident:
        existing = session.scalar(
            select(Incident)
            .where(Incident.code == alert.code)
            .where(Incident.status != IncidentStatus.RESOLVED.value)
            .order_by(Incident.created_at.desc())
            .limit(1)
        )
        if existing is not None:
            return existing

        incident = Incident(
            code=alert.code,
            title=alert.title,
            detail=alert.detail,
            severity=alert.severity.value,
            status=IncidentStatus.OPEN.value,
            created_at=alert.occurred_at,
        )
        session.add(incident)
        session.commit()
        session.refresh(incident)

        notifier.send(alert)
        return incident

    def list_incidents(
        self,
        session: Session,
        *,
        limit: int = 100,
    ) -> list[Incident]:
        safe_limit = min(max(limit, 1), 100)
        return list(
            session.scalars(
                select(Incident).order_by(Incident.created_at.desc()).limit(safe_limit)
            ).all()
        )

    def acknowledge(
        self,
        session: Session,
        incident_id: int,
    ) -> Incident:
        incident = self._get(session, incident_id)
        if incident.status == IncidentStatus.RESOLVED.value:
            raise InvalidIncidentStateError("Resolved incident cannot be acknowledged")

        incident.status = IncidentStatus.ACKNOWLEDGED.value
        incident.acknowledged_at = datetime.now(UTC)
        session.commit()
        session.refresh(incident)
        return incident

    def resolve(
        self,
        session: Session,
        incident_id: int,
    ) -> Incident:
        incident = self._get(session, incident_id)
        if incident.status == IncidentStatus.RESOLVED.value:
            return incident

        incident.status = IncidentStatus.RESOLVED.value
        incident.resolved_at = datetime.now(UTC)
        session.commit()
        session.refresh(incident)
        return incident

    @staticmethod
    def _get(
        session: Session,
        incident_id: int,
    ) -> Incident:
        incident = session.get(Incident, incident_id)
        if incident is None:
            raise IncidentNotFoundError(f"Incident not found: {incident_id}")
        return incident
