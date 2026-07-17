from sqlalchemy import select
from sqlalchemy.orm import Session

from .authorization_models import AuthorizationEvent
from .scopes import ApiScope
from .security import Principal


class AuthorizationAuditService:
    def record(
        self,
        session: Session,
        *,
        principal: Principal,
        method: str,
        path: str,
        required_scope: ApiScope | None,
        allowed: bool,
        detail: str | None = None,
    ) -> AuthorizationEvent:
        event = AuthorizationEvent(
            api_key_id=principal.api_key_id,
            method=method.upper(),
            path=path,
            required_scope=(required_scope.value if required_scope is not None else None),
            decision="allow" if allowed else "deny",
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
    ) -> list[AuthorizationEvent]:
        return list(
            session.scalars(
                select(AuthorizationEvent)
                .order_by(AuthorizationEvent.created_at.desc())
                .limit(min(max(limit, 1), 100))
            ).all()
        )
