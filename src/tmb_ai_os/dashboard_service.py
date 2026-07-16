from dataclasses import asdict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .backup_factory import create_backup_manager
from .health import build_readiness_report
from .incident_models import Incident
from .notification_models import NotificationDelivery
from .operations_metrics import get_operations_metrics


class DashboardService:
    def summary(self, session: Session) -> dict[str, object]:
        readiness = build_readiness_report(session)
        metrics = get_operations_metrics(session)
        backups = create_backup_manager().list()

        open_incidents = session.scalar(
            select(func.count()).select_from(Incident).where(Incident.status != "resolved")
        )
        failed_deliveries = session.scalar(
            select(func.count())
            .select_from(NotificationDelivery)
            .where(NotificationDelivery.status == "failed")
        )

        return {
            "readiness": {
                "ready": readiness.ready,
                "checks": [asdict(item) for item in readiness.checks],
            },
            "metrics": asdict(metrics),
            "incidents": {"open": int(open_incidents or 0)},
            "backups": {
                "count": len(backups),
                "latest": backups[0].created_at if backups else None,
            },
            "notifications": {
                "failed": int(failed_deliveries or 0),
            },
        }

    def incidents(
        self,
        session: Session,
        *,
        limit: int = 20,
    ) -> list[dict[str, object]]:
        rows = session.scalars(
            select(Incident).order_by(Incident.created_at.desc()).limit(min(max(limit, 1), 100))
        ).all()
        return [
            {
                "id": item.id,
                "code": item.code,
                "title": item.title,
                "severity": item.severity,
                "status": item.status,
                "created_at": item.created_at,
            }
            for item in rows
        ]

    def notifications(
        self,
        session: Session,
        *,
        limit: int = 20,
    ) -> list[dict[str, object]]:
        rows = session.scalars(
            select(NotificationDelivery)
            .order_by(NotificationDelivery.created_at.desc())
            .limit(min(max(limit, 1), 100))
        ).all()
        return [
            {
                "id": item.id,
                "provider": item.provider,
                "alert_code": item.alert_code,
                "status": item.status,
                "response_code": item.response_code,
                "created_at": item.created_at,
            }
            for item in rows
        ]
