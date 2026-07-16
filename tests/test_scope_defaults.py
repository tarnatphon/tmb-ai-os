from tmb_ai_os.scopes import (
    ApiScope,
    default_scopes_for_role,
)
from tmb_ai_os.security import Role


def test_admin_has_all_scopes() -> None:
    assert default_scopes_for_role(Role.ADMIN) == frozenset(ApiScope)


def test_viewer_has_read_only_scopes() -> None:
    scopes = default_scopes_for_role(Role.VIEWER)

    assert ApiScope.DASHBOARD_READ in scopes
    assert ApiScope.CONTENT_WRITE not in scopes
