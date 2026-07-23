"""Alert dashboard API for Milestone 6.13."""

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from .alert_observability import AlertMetricsSnapshot, get_alert_metrics
from .security import Permission, Principal
from .unified_auth import unified_permission_dependency

router = APIRouter(prefix="/v27", tags=["Milestone 6.13"])

SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(unified_permission_dependency(Permission.SECURITY_ADMIN)),
]


class AlertDeliverySummary(BaseModel):
    success_total: int = Field(ge=0)
    failed_total: int = Field(ge=0)
    suppressed_total: int = Field(ge=0)
    attempted_total: int = Field(ge=0)
    success_rate: float = Field(ge=0.0, le=1.0)


class AlertRoutingSummary(BaseModel):
    routed_total: int = Field(ge=0)
    fallback_total: int = Field(ge=0)
    no_route_total: int = Field(ge=0)


class AlertDashboardResponse(BaseModel):
    routing: AlertRoutingSummary
    delivery: AlertDeliverySummary
    generated_at: datetime


def build_alert_dashboard(
    snapshot: AlertMetricsSnapshot,
) -> AlertDashboardResponse:
    attempted_total = (
        snapshot.delivery_success_total
        + snapshot.delivery_failed_total
        + snapshot.delivery_suppressed_total
    )

    success_rate = snapshot.delivery_success_total / attempted_total if attempted_total > 0 else 0.0

    return AlertDashboardResponse(
        routing=AlertRoutingSummary(
            routed_total=snapshot.routed_total,
            fallback_total=snapshot.fallback_total,
            no_route_total=snapshot.no_route_total,
        ),
        delivery=AlertDeliverySummary(
            success_total=snapshot.delivery_success_total,
            failed_total=snapshot.delivery_failed_total,
            suppressed_total=snapshot.delivery_suppressed_total,
            attempted_total=attempted_total,
            success_rate=success_rate,
        ),
        generated_at=datetime.now(UTC),
    )


@router.get(
    "/admin/dashboard/alerts",
    response_model=AlertDashboardResponse,
)
def alert_dashboard(
    _: SecurityAdminPrincipal,
) -> AlertDashboardResponse:
    """Return the current shared alert-routing metrics summary."""
    return build_alert_dashboard(get_alert_metrics())
