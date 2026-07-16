from sqlalchemy.orm import Session

from .security import Principal
from .security_service import SecurityAuditService


def record_authentication_success(
    session: Session,
    *,
    principal: Principal,
    action: str,
) -> None:
    SecurityAuditService().record(
        session,
        principal=principal,
        action=action,
        outcome="success",
        detail=f"Authenticated with key {principal.api_key_id}",
    )
