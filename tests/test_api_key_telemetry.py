from datetime import UTC, datetime

from sqlalchemy.orm import Session

from tmb_ai_os.api_key_telemetry import (
    ApiKeyTelemetryService,
)
from tmb_ai_os.database import Base, build_engine


def test_records_and_summarizes_key_risk() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    service = ApiKeyTelemetryService()

    for index in range(10):
        service.record(
            session,
            api_key_id="risky-key",
            method="GET",
            path="/v4/content",
            status_code=401 if index < 6 else 200,
            client_ip=f"10.0.0.{index + 1}",
            occurred_at=datetime.now(UTC),
        )

    summary = service.summarize_risk(
        session,
        api_key_id="risky-key",
    )

    assert summary.total_requests == 10
    assert summary.failed_requests == 6
    assert summary.distinct_ips == 10
    assert summary.risk_score == 65
    assert "high_failure_ratio" in summary.reasons
    assert "many_source_ips" in summary.reasons

    session.close()


def test_recent_events_are_limited() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)
    service = ApiKeyTelemetryService()

    for _ in range(3):
        service.record(
            session,
            api_key_id="normal-key",
            method="POST",
            path="/v7/publish",
            status_code=200,
        )

    events = service.recent_events(
        session,
        api_key_id="normal-key",
        limit=2,
    )

    assert len(events) == 2
    session.close()
