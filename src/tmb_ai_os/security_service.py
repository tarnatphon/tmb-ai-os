from sqlalchemy import select
from sqlalchemy.orm import Session

from .security import Principal
from .security_models import SecurityAuditEvent


class SecurityAuditService:
    def record(
        self,
        session: Session,
        *,
        principal: Principal,
        action: str,
        outcome: str,
        detail: str | None = None,
    ) -> SecurityAuditEvent:
        event = SecurityAuditEvent(
            actor=principal.api_key_id,
            role=principal.role.value,
            action=action,
            outcome=outcome,
            detail=detail,
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    def list_events(
        self,
        session: Session,
        *,
        limit: int = 100,
    ) -> list[SecurityAuditEvent]:
        safe_limit = min(max(limit, 1), 100)
        return list(
            session.scalars(
                select(SecurityAuditEvent)
                .order_by(SecurityAuditEvent.created_at.desc())
                .limit(safe_limit)
            ).all()
        )
