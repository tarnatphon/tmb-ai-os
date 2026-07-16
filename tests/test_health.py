from sqlalchemy.orm import Session

from tmb_ai_os.database import Base, build_engine
from tmb_ai_os.health import (
    build_readiness_report,
    check_database,
)


def test_database_health_check_passes() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    result = check_database(session)

    assert result.healthy is True
    session.close()


def test_readiness_report_is_ready() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    report = build_readiness_report(session)

    assert report.ready is True
    session.close()
