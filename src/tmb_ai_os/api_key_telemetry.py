from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .api_key_telemetry_models import ApiKeyUsageEvent


@dataclass(frozen=True)
class ApiKeyRiskSummary:
    api_key_id: str
    total_requests: int
    failed_requests: int
    distinct_ips: int
    risk_score: int
    reasons: tuple[str, ...]


class ApiKeyTelemetryService:
    def record(
        self,
        session: Session,
        *,
        api_key_id: str,
        method: str,
        path: str,
        status_code: int,
        client_ip: str | None = None,
        occurred_at: datetime | None = None,
    ) -> ApiKeyUsageEvent:
        event = ApiKeyUsageEvent(
            api_key_id=api_key_id,
            method=method.upper(),
            path=path,
            status_code=status_code,
            client_ip=client_ip,
            occurred_at=occurred_at or datetime.now(UTC),
        )
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    def summarize_risk(
        self,
        session: Session,
        *,
        api_key_id: str,
        window_minutes: int = 60,
    ) -> ApiKeyRiskSummary:
        since = datetime.now(UTC) - timedelta(minutes=max(window_minutes, 1))

        total_requests = (
            session.scalar(
                select(func.count(ApiKeyUsageEvent.id)).where(
                    ApiKeyUsageEvent.api_key_id == api_key_id,
                    ApiKeyUsageEvent.occurred_at >= since,
                )
            )
            or 0
        )

        failed_requests = (
            session.scalar(
                select(func.count(ApiKeyUsageEvent.id)).where(
                    ApiKeyUsageEvent.api_key_id == api_key_id,
                    ApiKeyUsageEvent.occurred_at >= since,
                    ApiKeyUsageEvent.status_code >= 400,
                )
            )
            or 0
        )

        distinct_ips = (
            session.scalar(
                select(func.count(func.distinct(ApiKeyUsageEvent.client_ip))).where(
                    ApiKeyUsageEvent.api_key_id == api_key_id,
                    ApiKeyUsageEvent.occurred_at >= since,
                    ApiKeyUsageEvent.client_ip.is_not(None),
                )
            )
            or 0
        )

        score = 0
        reasons: list[str] = []

        if total_requests >= 500:
            score += 40
            reasons.append("high_request_volume")

        if total_requests > 0:
            failure_ratio = failed_requests / total_requests
            if failure_ratio >= 0.5:
                score += 35
                reasons.append("high_failure_ratio")
            elif failure_ratio >= 0.2:
                score += 20
                reasons.append("elevated_failure_ratio")

        if distinct_ips >= 10:
            score += 30
            reasons.append("many_source_ips")
        elif distinct_ips >= 5:
            score += 15
            reasons.append("multiple_source_ips")

        return ApiKeyRiskSummary(
            api_key_id=api_key_id,
            total_requests=total_requests,
            failed_requests=failed_requests,
            distinct_ips=distinct_ips,
            risk_score=min(score, 100),
            reasons=tuple(reasons),
        )

    def recent_events(
        self,
        session: Session,
        *,
        api_key_id: str,
        limit: int = 100,
    ) -> list[ApiKeyUsageEvent]:
        safe_limit = min(max(limit, 1), 500)
        return list(
            session.scalars(
                select(ApiKeyUsageEvent)
                .where(ApiKeyUsageEvent.api_key_id == api_key_id)
                .order_by(ApiKeyUsageEvent.occurred_at.desc())
                .limit(safe_limit)
            ).all()
        )
