from datetime import UTC, datetime, timedelta

import pytest

from tmb_ai_os.retention import RetentionPolicy


def test_retention_policy_cutoffs() -> None:
    policy = RetentionPolicy(
        content_days=10,
        audit_days=5,
        backup_days=2,
    )
    now = datetime.now(UTC)

    assert policy.content_cutoff(now=now) == (now - timedelta(days=10))
    assert policy.audit_cutoff(now=now) == (now - timedelta(days=5))


def test_retention_policy_rejects_zero_days() -> None:
    with pytest.raises(ValueError):
        RetentionPolicy(content_days=0)
