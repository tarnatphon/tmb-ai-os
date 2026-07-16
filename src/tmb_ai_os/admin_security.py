from dataclasses import dataclass

from .security import Permission, Principal, require_permission


@dataclass(frozen=True)
class AdminSession:
    api_key_id: str
    role: str
    authenticated: bool


def validate_admin_principal(
    principal: Principal,
) -> AdminSession:
    require_permission(
        principal,
        Permission.SECURITY_ADMIN,
    )

    return AdminSession(
        api_key_id=principal.api_key_id,
        role=principal.role.value,
        authenticated=True,
    )
