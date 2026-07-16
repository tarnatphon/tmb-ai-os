import hashlib
import secrets
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from .api_key_models import ManagedApiKey
from .security import Principal, Role


@dataclass(frozen=True)
class CreatedApiKey:
    key_id: str
    plaintext_key: str
    role: str
    expires_at: datetime | None


class ApiKeyNotFoundError(LookupError):
    pass


class ApiKeyService:
    def create(
        self,
        session: Session,
        *,
        key_id: str,
        role: Role,
        expires_in_days: int | None = None,
    ) -> CreatedApiKey:
        existing = session.scalar(select(ManagedApiKey).where(ManagedApiKey.key_id == key_id))
        if existing is not None:
            raise ValueError(f"API key ID already exists: {key_id}")

        plaintext = secrets.token_urlsafe(32)
        expires_at = (
            datetime.now(UTC) + timedelta(days=expires_in_days)
            if expires_in_days is not None
            else None
        )

        row = ManagedApiKey(
            key_id=key_id,
            key_hash=self.hash_key(plaintext),
            role=role.value,
            active=True,
            expires_at=expires_at,
        )
        session.add(row)
        session.commit()

        return CreatedApiKey(
            key_id=key_id,
            plaintext_key=plaintext,
            role=role.value,
            expires_at=expires_at,
        )

    def list(self, session: Session) -> list[ManagedApiKey]:
        return list(
            session.scalars(select(ManagedApiKey).order_by(ManagedApiKey.created_at.desc())).all()
        )

    def authenticate(
        self,
        session: Session,
        plaintext_key: str,
    ) -> Principal | None:
        row = session.scalar(
            select(ManagedApiKey).where(ManagedApiKey.key_hash == self.hash_key(plaintext_key))
        )
        if row is None or not row.active:
            return None

        if row.expires_at is not None and row.expires_at < datetime.now(UTC):
            return None

        return Principal(
            api_key_id=row.key_id,
            role=Role(row.role),
        )

    def revoke(
        self,
        session: Session,
        key_id: str,
    ) -> ManagedApiKey:
        row = self._get(session, key_id)
        row.active = False
        row.revoked_at = datetime.now(UTC)
        session.commit()
        session.refresh(row)
        return row

    def rotate(
        self,
        session: Session,
        key_id: str,
    ) -> CreatedApiKey:
        row = self._get(session, key_id)
        plaintext = secrets.token_urlsafe(32)
        row.key_hash = self.hash_key(plaintext)
        row.active = True
        row.revoked_at = None
        session.commit()

        return CreatedApiKey(
            key_id=row.key_id,
            plaintext_key=plaintext,
            role=row.role,
            expires_at=row.expires_at,
        )

    @staticmethod
    def hash_key(plaintext_key: str) -> str:
        return hashlib.sha256(plaintext_key.encode("utf-8")).hexdigest()

    @staticmethod
    def _get(
        session: Session,
        key_id: str,
    ) -> ManagedApiKey:
        row = session.scalar(select(ManagedApiKey).where(ManagedApiKey.key_id == key_id))
        if row is None:
            raise ApiKeyNotFoundError(f"API key not found: {key_id}")
        return row
