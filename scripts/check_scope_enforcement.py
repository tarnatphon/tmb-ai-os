from tmb_ai_os.scopes import ApiScope
from tmb_ai_os.security_policies import (
    required_scope_for_route,
)

EXPECTED_POLICIES = (
    (
        "GET",
        "/v18/dashboard/summary",
        ApiScope.DASHBOARD_READ,
    ),
    (
        "GET",
        "/v4/content",
        ApiScope.CONTENT_READ,
    ),
    (
        "POST",
        "/v4/content",
        ApiScope.CONTENT_WRITE,
    ),
    (
        "POST",
        "/v7/publish",
        ApiScope.PUBLISH_RUN,
    ),
    (
        "POST",
        "/v16/incidents",
        ApiScope.INCIDENT_MANAGE,
    ),
    (
        "POST",
        "/v17/incidents",
        ApiScope.INCIDENT_MANAGE,
    ),
    (
        "GET",
        "/v20/api-keys",
        ApiScope.SECURITY_ADMIN,
    ),
    (
        "POST",
        "/v20/api-keys",
        ApiScope.SECURITY_ADMIN,
    ),
)


def main() -> None:
    failures: list[str] = []

    for method, path, expected_scope in EXPECTED_POLICIES:
        actual_scope = required_scope_for_route(
            method=method,
            path=path,
        )

        if actual_scope is not expected_scope:
            failures.append(
                f"{method} {path}: expected "
                f"{expected_scope.value}, got "
                f"{actual_scope.value if actual_scope else 'none'}"
            )

    if failures:
        raise SystemExit("Scope enforcement validation failed:\n" + "\n".join(failures))

    print("Scope enforcement check passed")


if __name__ == "__main__":
    main()
