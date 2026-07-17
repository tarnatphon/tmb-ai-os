from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .database import get_db
from .scoped_auth import scope_dependency
from .scopes import ApiScope
from .security import Principal
from .security_policies import (
    ROUTE_SCOPE_POLICIES,
    required_scope_for_route,
)

router = APIRouter(prefix="/v23", tags=["Milestone 6.4"])
DbSession = Annotated[Session, Depends(get_db)]
SecurityAdminPrincipal = Annotated[
    Principal,
    Depends(scope_dependency(ApiScope.SECURITY_ADMIN)),
]


class PolicyCheckRequest(BaseModel):
    method: str
    path: str


@router.get("/security/policies")
def list_security_policies(
    _: SecurityAdminPrincipal,
) -> list[dict[str, str]]:
    return [
        {
            "method": policy.method,
            "path_prefix": policy.path_prefix,
            "scope": policy.scope.value,
        }
        for policy in ROUTE_SCOPE_POLICIES
    ]


@router.post("/security/check")
def check_security_policy(
    payload: PolicyCheckRequest,
    _: SecurityAdminPrincipal,
) -> dict[str, str | None]:
    required = required_scope_for_route(
        method=payload.method,
        path=payload.path,
    )
    return {
        "method": payload.method.upper(),
        "path": payload.path,
        "required_scope": (required.value if required is not None else None),
    }
