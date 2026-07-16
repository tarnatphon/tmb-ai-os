import shutil
from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from .audit_models import ContentAuditEvent
from .backups import BackupManager
from .models import ContentRun
from .retention import RetentionPolicy
from .security_models import SecurityAuditEvent


@dataclass(frozen=True)
class MaintenancePreview:
    content_rows: int
    content_audit_rows: int
    security_audit_rows: int
    backup_directories: tuple[str, ...]


@dataclass(frozen=True)
class MaintenanceResult:
    deleted_content_rows: int
    deleted_content_audit_rows: int
    deleted_security_audit_rows: int
    deleted_backup_directories: tuple[str, ...]


class MaintenanceConfirmationError(PermissionError):
    pass


class MaintenanceService:
    def __init__(
        self,
        *,
        policy: RetentionPolicy,
        backup_manager: BackupManager,
    ) -> None:
        self.policy = policy
        self.backup_manager = backup_manager

    def preview(
        self,
        session: Session,
        *,
        now: datetime | None = None,
    ) -> MaintenancePreview:
        current = now or datetime.now(UTC)

        content_ids = list(
            session.scalars(
                select(ContentRun.id).where(
                    ContentRun.created_at < self.policy.content_cutoff(now=current)
                )
            ).all()
        )

        content_audit_count = len(
            session.scalars(
                select(ContentAuditEvent.id).where(
                    ContentAuditEvent.created_at < self.policy.audit_cutoff(now=current)
                )
            ).all()
        )

        security_audit_count = len(
            session.scalars(
                select(SecurityAuditEvent.id).where(
                    SecurityAuditEvent.created_at < self.policy.audit_cutoff(now=current)
                )
            ).all()
        )

        return MaintenancePreview(
            content_rows=len(content_ids),
            content_audit_rows=content_audit_count,
            security_audit_rows=security_audit_count,
            backup_directories=self._expired_backups(current),
        )

    def run(
        self,
        session: Session,
        *,
        confirm: bool,
        now: datetime | None = None,
    ) -> MaintenanceResult:
        if not confirm:
            raise MaintenanceConfirmationError("Maintenance purge requires confirmation")

        current = now or datetime.now(UTC)
        preview = self.preview(session, now=current)

        session.execute(
            delete(ContentAuditEvent).where(
                ContentAuditEvent.created_at < self.policy.audit_cutoff(now=current)
            )
        )
        session.execute(
            delete(SecurityAuditEvent).where(
                SecurityAuditEvent.created_at < self.policy.audit_cutoff(now=current)
            )
        )
        session.execute(
            delete(ContentRun).where(
                ContentRun.created_at < self.policy.content_cutoff(now=current)
            )
        )

        for backup_name in preview.backup_directories:
            backup_path = self.backup_manager.backup_dir / backup_name
            shutil.rmtree(backup_path, ignore_errors=False)

        session.commit()

        return MaintenanceResult(
            deleted_content_rows=preview.content_rows,
            deleted_content_audit_rows=preview.content_audit_rows,
            deleted_security_audit_rows=preview.security_audit_rows,
            deleted_backup_directories=(preview.backup_directories),
        )

    def _expired_backups(
        self,
        now: datetime,
    ) -> tuple[str, ...]:
        cutoff = self.policy.backup_cutoff(now=now)
        expired: list[str] = []

        for manifest in self.backup_manager.list():
            try:
                created_at = datetime.fromisoformat(manifest.created_at)
            except ValueError:
                continue

            if created_at.tzinfo is None:
                created_at = created_at.replace(tzinfo=UTC)

            if created_at < cutoff:
                expired.append(manifest.name)

        return tuple(expired)
