import pytest

from tmb_ai_os.security import (
    AuthorizationError,
    Permission,
    Principal,
    Role,
    require_permission,
    verify_api_key,
)


def test_verify_api_key() -> None:
    assert verify_api_key("secret", "secret") is True
    assert verify_api_key("wrong", "secret") is False


def test_require_permission_allows_admin() -> None:
    principal = Principal(
        api_key_id="primary",
        role=Role.ADMIN,
    )

    require_permission(
        principal,
        Permission.SECURITY_ADMIN,
    )


def test_require_permission_rejects_viewer() -> None:
    principal = Principal(
        api_key_id="primary",
        role=Role.VIEWER,
    )

    with pytest.raises(AuthorizationError):
        require_permission(
            principal,
            Permission.CONTENT_APPROVE,
        )
