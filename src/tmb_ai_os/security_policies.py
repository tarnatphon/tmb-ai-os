from dataclasses import dataclass

from .scopes import ApiScope


@dataclass(frozen=True)
class RouteScopePolicy:
    method: str
    path_prefix: str
    scope: ApiScope


ROUTE_SCOPE_POLICIES: tuple[RouteScopePolicy, ...] = (
    RouteScopePolicy("GET", "/v18/dashboard", ApiScope.DASHBOARD_READ),
    RouteScopePolicy("GET", "/v4/content", ApiScope.CONTENT_READ),
    RouteScopePolicy("POST", "/v4/content", ApiScope.CONTENT_WRITE),
    RouteScopePolicy("POST", "/v7/publish", ApiScope.PUBLISH_RUN),
    RouteScopePolicy(
        "POST",
        "/v16/incidents",
        ApiScope.INCIDENT_MANAGE,
    ),
    RouteScopePolicy(
        "POST",
        "/v17/incidents",
        ApiScope.INCIDENT_MANAGE,
    ),
    RouteScopePolicy("GET", "/v20/api-keys", ApiScope.SECURITY_ADMIN),
    RouteScopePolicy("POST", "/v20/api-keys", ApiScope.SECURITY_ADMIN),
    RouteScopePolicy("GET", "/v22", ApiScope.SECURITY_ADMIN),
    RouteScopePolicy("PUT", "/v22", ApiScope.SECURITY_ADMIN),
)


def required_scope_for_route(
    *,
    method: str,
    path: str,
) -> ApiScope | None:
    normalized_method = method.upper()
    for policy in ROUTE_SCOPE_POLICIES:
        if policy.method == normalized_method and path.startswith(policy.path_prefix):
            return policy.scope
    return None
