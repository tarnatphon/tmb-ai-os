import json
import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .config import get_settings
from .rate_limit import InMemoryRateLimiter
from .request_context import (
    create_request_id,
    set_request_id,
)

logger = logging.getLogger("tmb_ai_os.access")

settings = get_settings()
rate_limiter = InMemoryRateLimiter(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)

CallNext = Callable[[Request], Awaitable[Response]]


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: CallNext,
    ) -> Response:
        request_id = request.headers.get(
            "X-Request-ID",
            create_request_id(),
        )
        set_request_id(request_id)

        started = time.perf_counter()
        response = await call_next(request)
        duration_ms = round(
            (time.perf_counter() - started) * 1000,
            2,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"

        logger.info(
            json.dumps(
                {
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                    "client": (request.client.host if request.client is not None else "unknown"),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )

        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: CallNext,
    ) -> Response:
        client_key = request.client.host if request.client is not None else "unknown"
        decision = rate_limiter.check(client_key)

        if not decision.allowed:
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Rate limit exceeded",
                    "reset_at": decision.reset_at.isoformat(),
                },
                headers={
                    "Retry-After": str(settings.rate_limit_window_seconds),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(decision.remaining)
        response.headers["X-RateLimit-Reset"] = decision.reset_at.isoformat()
        return response
