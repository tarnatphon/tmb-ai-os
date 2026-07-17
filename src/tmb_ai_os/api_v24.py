from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .authorization_audit import AuthorizationAuditService
from .database import get_db
from .policy_compliance import build_policy_compliance_report
from .scoped_auth import scope_dependency
from .scopes import ApiScope
from .security import Principal

router = APIRouter(prefix="/v24", tags=["Milestone 6.5"])
DbSession = Annotated[Session, Depends(get_db)]
SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(scope_dependency(ApiScope.SECURITY_ADMIN)),
]


@router.get("/security/authorization-events")
def list_authorization_events(
    _: SecurityAdminPrincipal,
    db: DbSession,
    limit: int = Query(default=100, ge=1, le=100),
) -> list[dict[str, object]]:
    return [
        {
            "id": row.id,
            "api_key_id": row.api_key_id,
            "method": row.method,
            "path": row.path,
            "required_scope": row.required_scope,
            "decision": row.decision,
            "detail": row.detail,
            "created_at": row.created_at,
        }
        for row in AuthorizationAuditService().list_events(
            db,
            limit=limit,
        )
    ]


@router.get("/security/policy-compliance")
def policy_compliance(
    _: SecurityAdminPrincipal,
) -> dict[str, object]:
    from .main import app

    report = build_policy_compliance_report(app)
    return {
        "protected_routes": report.protected_routes,
        "covered_routes": report.covered_routes,
        "gap_count": len(report.gaps),
        "gaps": [{"method": gap.method, "path": gap.path} for gap in report.gaps],
    }
