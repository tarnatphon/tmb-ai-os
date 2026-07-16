from enum import StrEnum

from .security import Role


class ApiScope(StrEnum):
    DASHBOARD_READ = "dashboard:read"
    CONTENT_READ = "content:read"
    CONTENT_WRITE = "content:write"
    PUBLISH_RUN = "publish:run"
    INCIDENT_MANAGE = "incident:manage"
    SECURITY_ADMIN = "security:admin"


ROLE_DEFAULT_SCOPES: dict[Role, frozenset[ApiScope]] = {
    Role.ADMIN: frozenset(ApiScope),
    Role.PUBLISHER: frozenset(
        {
            ApiScope.CONTENT_READ,
            ApiScope.CONTENT_WRITE,
            ApiScope.PUBLISH_RUN,
            ApiScope.DASHBOARD_READ,
        }
    ),
    Role.VIEWER: frozenset(
        {
            ApiScope.CONTENT_READ,
            ApiScope.DASHBOARD_READ,
        }
    ),
}


def default_scopes_for_role(role: Role) -> frozenset[ApiScope]:
    return ROLE_DEFAULT_SCOPES[role]
