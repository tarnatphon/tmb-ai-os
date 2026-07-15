from datetime import UTC, datetime, timedelta

from tmb_ai_os.retry_policy import RetryPolicy


def test_retry_policy_uses_exponential_backoff() -> None:
    policy = RetryPolicy(
        max_attempts=3,
        base_delay_seconds=60,
    )
    now = datetime.now(UTC)

    first = policy.next_retry_at(1, now=now)
    second = policy.next_retry_at(2, now=now)

    assert first == now + timedelta(seconds=60)
    assert second == now + timedelta(seconds=120)
    assert policy.can_retry(2) is True
    assert policy.can_retry(3) is False
