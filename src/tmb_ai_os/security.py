import hmac
from dataclasses import dataclass
from enum import StrEnum


class Role(StrEnum):
    VIEWER = "viewer"
    REVIEWER = "reviewer"
    MANAGER = "manager"
    PUBLISHER = "publisher"
    ADMIN = "admin"


class Permission(StrEnum):
    CONTENT_READ = "content_read"
    CONTENT_REVIEW = "content_review"
    CONTENT_APPROVE = "content_approve"
    CONTENT_PUBLISH = "content_publish"
    OPERATIONS_READ = "operations_read"
    SECURITY_ADMIN = "security_admin"


ROLE_PERMISSIONS: dict[Role, set[Permission]] = {
    Role.VIEWER: {
        Permission.CONTENT_READ,
        Permission.OPERATIONS_READ,
    },
    Role.REVIEWER: {
        Permission.CONTENT_READ,
        Permission.CONTENT_REVIEW,
        Permission.OPERATIONS_READ,
    },
    Role.MANAGER: {
        Permission.CONTENT_READ,
        Permission.CONTENT_REVIEW,
        Permission.CONTENT_APPROVE,
        Permission.OPERATIONS_READ,
    },
    Role.PUBLISHER: {
        Permission.CONTENT_READ,
        Permission.CONTENT_PUBLISH,
        Permission.OPERATIONS_READ,
    },
    Role.ADMIN: set(Permission),
}


@dataclass(frozen=True)
class Principal:
    api_key_id: str
    role: Role


class AuthenticationError(PermissionError):
    pass


class AuthorizationError(PermissionError):
    pass


def verify_api_key(
    supplied: str,
    expected: str,
) -> bool:
    if not supplied or not expected:
        return False
    return hmac.compare_digest(supplied, expected)


def require_permission(
    principal: Principal,
    permission: Permission,
) -> None:
    if permission not in ROLE_PERMISSIONS[principal.role]:
        raise AuthorizationError(f"Role {principal.role} lacks permission {permission}")
