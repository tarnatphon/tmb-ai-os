from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .api_key_telemetry import ApiKeyTelemetryService
from .database import get_db
from .scoped_auth import scope_dependency
from .scopes import ApiScope
from .security import Principal

router = APIRouter(prefix="/v26", tags=["Milestone 6.7"])
DbSession = Annotated[Session, Depends(get_db)]
SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(scope_dependency(ApiScope.SECURITY_ADMIN)),
]


@router.get("/security/api-key-telemetry/{api_key_id}/risk")
def get_key_risk(
    api_key_id: str,
    _: SecurityAdminPrincipal,
    db: DbSession,
    window_minutes: int = Query(
        default=60,
        ge=1,
        le=1440,
    ),
) -> dict[str, object]:
    summary = ApiKeyTelemetryService().summarize_risk(
        db,
        api_key_id=api_key_id,
        window_minutes=window_minutes,
    )
    return {
        "api_key_id": summary.api_key_id,
        "total_requests": summary.total_requests,
        "failed_requests": summary.failed_requests,
        "distinct_ips": summary.distinct_ips,
        "risk_score": summary.risk_score,
        "reasons": list(summary.reasons),
    }


@router.get("/security/api-key-telemetry/{api_key_id}/events")
def get_key_events(
    api_key_id: str,
    _: SecurityAdminPrincipal,
    db: DbSession,
    limit: int = Query(default=100, ge=1, le=500),
) -> list[dict[str, object]]:
    return [
        {
            "method": event.method,
            "path": event.path,
            "status_code": event.status_code,
            "client_ip": event.client_ip,
            "occurred_at": event.occurred_at,
        }
        for event in ApiKeyTelemetryService().recent_events(
            db,
            api_key_id=api_key_id,
            limit=limit,
        )
    ]
