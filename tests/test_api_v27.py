from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from tmb_ai_os.alert_observability import (
    AlertMetricsSnapshot,
    reset_alert_metrics,
)
from tmb_ai_os.api import app
from tmb_ai_os.api_v27 import build_alert_dashboard


@pytest.fixture(autouse=True)
def reset_shared_alert_metrics() -> None:
    reset_alert_metrics()
    yield
    reset_alert_metrics()


def test_build_alert_dashboard_with_empty_metrics() -> None:
    response = build_alert_dashboard(
        AlertMetricsSnapshot(
            routed_total=0,
            delivery_success_total=0,
            delivery_failed_total=0,
            delivery_suppressed_total=0,
            fallback_total=0,
            no_route_total=0,
        )
    )

    assert response.routing.routed_total == 0
    assert response.routing.fallback_total == 0
    assert response.routing.no_route_total == 0

    assert response.delivery.success_total == 0
    assert response.delivery.failed_total == 0
    assert response.delivery.suppressed_total == 0
    assert response.delivery.attempted_total == 0
    assert response.delivery.success_rate == 0.0

    assert isinstance(response.generated_at, datetime)


def test_build_alert_dashboard_aggregates_delivery_metrics() -> None:
    response = build_alert_dashboard(
        AlertMetricsSnapshot(
            routed_total=8,
            delivery_success_total=6,
            delivery_failed_total=2,
            delivery_suppressed_total=2,
            fallback_total=3,
            no_route_total=1,
        )
    )

    assert response.routing.routed_total == 8
    assert response.routing.fallback_total == 3
    assert response.routing.no_route_total == 1

    assert response.delivery.success_total == 6
    assert response.delivery.failed_total == 2
    assert response.delivery.suppressed_total == 2
    assert response.delivery.attempted_total == 10
    assert response.delivery.success_rate == pytest.approx(0.6)


def test_alert_dashboard_requires_authentication() -> None:
    with TestClient(app) as client:
        response = client.get("/v27/admin/dashboard/alerts")

    assert response.status_code == 401
    assert response.json() == {"detail": "Missing API key"}


def test_v27_router_exposes_alert_dashboard_route() -> None:
    assert "/v27/admin/dashboard/alerts" in app.openapi()["paths"]
