from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.orm import Session

from tmb_ai_os.api_key_lifecycle import (
    ApiKeyLifecycleError,
    ApiKeyLifecycleService,
)
from tmb_ai_os.database import Base, build_engine


def test_expired_key_is_rejected() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    service = ApiKeyLifecycleService()
    service.configure(
        session,
        api_key_id="expired-key",
        expires_at=datetime.now(UTC) - timedelta(minutes=1),
    )

    with pytest.raises(ApiKeyLifecycleError):
        service.enforce(
            session,
            api_key_id="expired-key",
        )

    session.close()


def test_rotation_requirement_is_enforced() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    session = Session(engine)

    service = ApiKeyLifecycleService()
    service.configure(
        session,
        api_key_id="rotation-key",
        rotation_required=True,
    )

    with pytest.raises(ApiKeyLifecycleError):
        service.enforce(
            session,
            api_key_id="rotation-key",
        )

    session.close()
