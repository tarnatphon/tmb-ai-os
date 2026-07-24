"""System health dashboard API for Phase 7.1."""

from typing import Annotated

from fastapi import APIRouter, Depends

from .security import Permission, Principal
from .system_health import SystemHealth, get_system_health
from .unified_auth import unified_permission_dependency

router = APIRouter(prefix="/v28", tags=["Phase 7.1"])

SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(unified_permission_dependency(Permission.SECURITY_ADMIN)),
]


@router.get(
    "/admin/dashboard/system-health",
    response_model=SystemHealth,
)
def system_health_dashboard(
    _: SecurityAdminPrincipal,
) -> SystemHealth:
    """Return the current application and runtime health summary."""
    return get_system_health()
