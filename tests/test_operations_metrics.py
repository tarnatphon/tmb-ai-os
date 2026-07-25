from sqlalchemy.orm import Session

from tmb_ai_os.audit_models import PublishQueueItem
from tmb_ai_os.content_history import ContentHistoryRepository
from tmb_ai_os.content_records import ContentCreate
from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.operations_metrics import (
    get_content_metrics,
    get_publish_queue_metrics,
)


def make_session() -> Session:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_content_metrics_count_statuses() -> None:
    session = make_session()
    ContentHistoryRepository().create(
        session,
        ContentCreate(
            topic="OEM Bags",
            channels={"facebook": "content"},
        ),
    )

    metrics = get_content_metrics(session)

    assert metrics.total == 1
    assert metrics.generated == 1
    session.close()


def test_publish_queue_metrics_count_statuses() -> None:
    session = make_session()
    session.add(
        PublishQueueItem(
            content_id=1,
            status="failed",
        )
    )
    session.commit()

    metrics = get_publish_queue_metrics(session)

    assert metrics.failed == 1
    session.close()


def test_ai_metrics_default_to_zero() -> None:
    from tmb_ai_os.operations_metrics import get_ai_metrics

    metrics = get_ai_metrics()

    assert metrics.requests == 0
    assert metrics.input_tokens == 0
    assert metrics.output_tokens == 0
    assert metrics.estimated_cost_usd == 0.0


def test_agent_metrics_default_to_zero() -> None:
    from tmb_ai_os.operations_metrics import get_agent_metrics

    metrics = get_agent_metrics()

    assert metrics.total_runs == 0
    assert metrics.successful_runs == 0
    assert metrics.failed_runs == 0


def test_workflow_metrics_default_to_zero() -> None:
    from tmb_ai_os.operations_metrics import get_workflow_metrics

    metrics = get_workflow_metrics()

    assert metrics.total_runs == 0
    assert metrics.active_runs == 0
    assert metrics.failed_runs == 0


def test_operations_metrics_include_platform_metrics() -> None:
    from tmb_ai_os.operations_metrics import get_operations_metrics

    session = make_session()

    metrics = get_operations_metrics(session)

    assert metrics.ai.requests == 0
    assert metrics.agents.total_runs == 0
    assert metrics.workflows.total_runs == 0

    session.close()
