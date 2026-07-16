from datetime import UTC, datetime, timedelta

from tmb_ai_os.rate_limit import InMemoryRateLimiter


def test_rate_limiter_blocks_after_limit() -> None:
    limiter = InMemoryRateLimiter(
        max_requests=2,
        window_seconds=60,
    )
    now = datetime.now(UTC)

    first = limiter.check("client", now=now)
    second = limiter.check(
        "client",
        now=now + timedelta(seconds=1),
    )
    third = limiter.check(
        "client",
        now=now + timedelta(seconds=2),
    )

    assert first.allowed is True
    assert second.allowed is True
    assert third.allowed is False
