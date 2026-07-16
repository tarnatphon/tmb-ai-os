from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth_audit import record_authentication_success
from .config import get_settings
from .database import get_db
from .security import Principal
from .unified_auth import authenticate_request

router = APIRouter(prefix="/v21", tags=["Milestone 6.2"])
DbSession = Annotated[Session, Depends(get_db)]
AuthenticatedPrincipal = Annotated[
    Principal,
    Depends(authenticate_request),
]


class AuthValidationResponse(BaseModel):
    authenticated: bool
    api_key_id: str
    role: str


@router.get("/auth/status")
def auth_status() -> dict[str, object]:
    settings = get_settings()
    return {
        "managed_keys_enabled": True,
        "legacy_fallback_enabled": (settings.legacy_api_key_fallback_enabled),
    }


@router.post("/auth/validate")
def validate_authentication(
    principal: AuthenticatedPrincipal,
    db: DbSession,
) -> AuthValidationResponse:
    record_authentication_success(
        db,
        principal=principal,
        action="auth.validate",
    )
    return AuthValidationResponse(
        authenticated=True,
        api_key_id=principal.api_key_id,
        role=principal.role.value,
    )
