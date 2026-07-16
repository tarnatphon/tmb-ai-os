import pytest

from tmb_ai_os.admin_security import validate_admin_principal
from tmb_ai_os.security import (
    AuthorizationError,
    Principal,
    Role,
)


def test_admin_principal_is_allowed() -> None:
    session = validate_admin_principal(
        Principal(
            api_key_id="primary",
            role=Role.ADMIN,
        )
    )

    assert session.authenticated is True
    assert session.role == "admin"


def test_viewer_is_rejected() -> None:
    with pytest.raises(AuthorizationError):
        validate_admin_principal(
            Principal(
                api_key_id="viewer",
                role=Role.VIEWER,
            )
        )
