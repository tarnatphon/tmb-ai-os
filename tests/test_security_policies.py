from tmb_ai_os.scopes import ApiScope
from tmb_ai_os.security_policies import required_scope_for_route


def test_dashboard_policy() -> None:
    assert (
        required_scope_for_route(
            method="GET",
            path="/v18/dashboard/summary",
        )
        is ApiScope.DASHBOARD_READ
    )


def test_api_key_policy() -> None:
    assert (
        required_scope_for_route(
            method="POST",
            path="/v20/api-keys",
        )
        is ApiScope.SECURITY_ADMIN
    )
