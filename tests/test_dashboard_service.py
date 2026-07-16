from sqlalchemy.orm import Session

from tmb_ai_os.dashboard_service import DashboardService
from tmb_ai_os.database import Base, build_engine


def test_dashboard_summary() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    summary = DashboardService().summary(session)

    assert "readiness" in summary
    assert "metrics" in summary
    assert "incidents" in summary
    session.close()
