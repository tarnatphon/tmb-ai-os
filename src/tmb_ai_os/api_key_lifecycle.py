from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from .api_key_lifecycle_models import ApiKeyLifecycle


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)

    return value.astimezone(UTC)


class ApiKeyLifecycleError(PermissionError):
    pass


@dataclass(frozen=True)
class LifecycleStatus:
    api_key_id: str
    expired: bool
    rotation_required: bool
    revoked: bool
    expires_at: datetime | None


class ApiKeyLifecycleService:
    def configure(
        self,
        session: Session,
        *,
        api_key_id: str,
        expires_at: datetime | None = None,
        rotation_required: bool = False,
    ) -> ApiKeyLifecycle:
        record = session.scalar(
            select(ApiKeyLifecycle).where(ApiKeyLifecycle.api_key_id == api_key_id)
        )

        if record is None:
            record = ApiKeyLifecycle(api_key_id=api_key_id)
            session.add(record)

        record.expires_at = expires_at
        record.rotation_required = rotation_required
        record.revoked_at = None
        session.commit()
        session.refresh(record)
        return record

    def revoke(
        self,
        session: Session,
        *,
        api_key_id: str,
    ) -> ApiKeyLifecycle:
        record = self._require_record(session, api_key_id)
        record.revoked_at = datetime.now(UTC)
        session.commit()
        session.refresh(record)
        return record

    def require_rotation(
        self,
        session: Session,
        *,
        api_key_id: str,
    ) -> ApiKeyLifecycle:
        record = self._require_record(session, api_key_id)
        record.rotation_required = True
        session.commit()
        session.refresh(record)
        return record

    def clear_rotation_requirement(
        self,
        session: Session,
        *,
        api_key_id: str,
    ) -> ApiKeyLifecycle:
        record = self._require_record(session, api_key_id)
        record.rotation_required = False
        session.commit()
        session.refresh(record)
        return record

    def status(
        self,
        session: Session,
        *,
        api_key_id: str,
        now: datetime | None = None,
    ) -> LifecycleStatus:
        record = session.scalar(
            select(ApiKeyLifecycle).where(ApiKeyLifecycle.api_key_id == api_key_id)
        )
        current = _as_utc(now) if now is not None else datetime.now(UTC)

        if record is None:
            return LifecycleStatus(
                api_key_id=api_key_id,
                expired=False,
                rotation_required=False,
                revoked=False,
                expires_at=None,
            )

        return LifecycleStatus(
            api_key_id=api_key_id,
            expired=(record.expires_at is not None and _as_utc(record.expires_at) <= current),
            rotation_required=record.rotation_required,
            revoked=record.revoked_at is not None,
            expires_at=record.expires_at,
        )

    def enforce(
        self,
        session: Session,
        *,
        api_key_id: str,
    ) -> None:
        status = self.status(session, api_key_id=api_key_id)

        if status.revoked:
            raise ApiKeyLifecycleError("API key has been revoked")
        if status.expired:
            raise ApiKeyLifecycleError("API key has expired")
        if status.rotation_required:
            raise ApiKeyLifecycleError("API key rotation is required")

    def expiring_within(
        self,
        session: Session,
        *,
        days: int = 30,
    ) -> list[ApiKeyLifecycle]:
        now = datetime.now(UTC)
        deadline = now + timedelta(days=max(days, 0))

        return list(
            session.scalars(
                select(ApiKeyLifecycle)
                .where(ApiKeyLifecycle.expires_at.is_not(None))
                .where(ApiKeyLifecycle.expires_at >= now)
                .where(ApiKeyLifecycle.expires_at <= deadline)
                .where(ApiKeyLifecycle.revoked_at.is_(None))
                .order_by(ApiKeyLifecycle.expires_at.asc())
            ).all()
        )

    def _require_record(
        self,
        session: Session,
        api_key_id: str,
    ) -> ApiKeyLifecycle:
        record = session.scalar(
            select(ApiKeyLifecycle).where(ApiKeyLifecycle.api_key_id == api_key_id)
        )
        if record is None:
            raise KeyError(f"Lifecycle record not found: {api_key_id}")
        return record
