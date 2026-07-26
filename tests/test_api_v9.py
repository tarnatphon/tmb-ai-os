from collections.abc import Generator

from fastapi import FastAPI
from fastapi.testclient import TestClient

from tmb_ai_os.api_v9 import router
from tmb_ai_os.database import get_db
from tmb_ai_os.operations_metrics import (
    AgentMetrics,
    AiMetrics,
    ContentMetrics,
    OperationsMetrics,
    PublishQueueMetrics,
    WorkflowMetrics,
)


def test_operations_metrics_endpoint_includes_workflow_metrics(
    monkeypatch,
) -> None:
    snapshot = OperationsMetrics(
        content=ContentMetrics(
            total=12,
            generated=4,
            reviewed=2,
            approved=3,
            rejected=1,
            queued=1,
            published=1,
        ),
        publish_queue=PublishQueueMetrics(
            queued=2,
            retrying=1,
            failed=1,
            published=8,
        ),
        audit_events=15,
        ai=AiMetrics(
            requests=20,
            input_tokens=1_000,
            output_tokens=500,
            estimated_cost_usd=0.25,
        ),
        agents=AgentMetrics(
            total_runs=10,
            successful_runs=8,
            failed_runs=2,
        ),
        workflows=WorkflowMetrics(
            total_runs=7,
            active_runs=2,
            failed_runs=1,
        ),
    )

    monkeypatch.setattr(
        "tmb_ai_os.api_v9.get_operations_metrics",
        lambda _db: snapshot,
    )

    def override_get_db() -> Generator[object, None, None]:
        yield object()

    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        response = client.get("/v9/metrics/operations")

    assert response.status_code == 200
    assert response.json()["workflows"] == {
        "total_runs": 7,
        "active_runs": 2,
        "failed_runs": 1,
    }
