from dataclasses import asdict
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session

from .alert_observability import get_alert_metrics
from .database import get_db
from .health import build_readiness_report
from .http_metrics import get_http_metrics
from .operations_metrics import (
    get_content_metrics,
    get_operations_metrics,
    get_publish_queue_metrics,
)
from .prometheus_metrics import render_prometheus_metrics

router = APIRouter(prefix="/v9", tags=["Milestone 5.0"])
DbSession = Annotated[Session, Depends(get_db)]


@router.get("/health/live")
def liveness() -> dict[str, str]:
    return {
        "status": "alive",
        "service": "tmb-ai-os",
    }


@router.get("/health/ready")
def readiness(db: DbSession) -> JSONResponse:
    report = build_readiness_report(db)
    return JSONResponse(
        content={
            "ready": report.ready,
            "checks": [asdict(check) for check in report.checks],
        },
        status_code=200 if report.ready else 503,
    )


@router.get("/metrics/operations")
def operations_metrics(db: DbSession) -> dict[str, object]:
    return asdict(get_operations_metrics(db))


@router.get("/metrics/publish-queue")
def publish_queue_metrics(db: DbSession) -> dict[str, int]:
    return asdict(get_publish_queue_metrics(db))


@router.get("/metrics/content")
def content_metrics(db: DbSession) -> dict[str, int]:
    return asdict(get_content_metrics(db))


@router.get("/metrics/http")
def http_request_metrics() -> dict[str, object]:
    return asdict(get_http_metrics())


@router.get("/metrics/prometheus")
def prometheus_metrics() -> Response:
    return Response(
        content=render_prometheus_metrics(
            get_http_metrics(),
            get_alert_metrics(),
        ),
        media_type="text/plain; version=0.0.4",
    )
