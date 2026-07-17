from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware

from .api_key_telemetry import ApiKeyTelemetryService
from .database import SessionLocal


class ApiKeyTelemetryMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[
            [Request],
            Awaitable[Response],
        ],
    ) -> Response:
        response = await call_next(request)

        api_key_id = getattr(
            request.state,
            "api_key_id",
            None,
        )
        if not api_key_id:
            return response

        session: Session = SessionLocal()
        try:
            ApiKeyTelemetryService().record(
                session,
                api_key_id=str(api_key_id),
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                client_ip=(request.client.host if request.client is not None else None),
            )
        finally:
            session.close()

        return response
