from .backup_factory import create_backup_manager
from .config import get_settings
from .maintenance import MaintenanceService
from .retention import RetentionPolicy


def create_maintenance_service() -> MaintenanceService:
    settings = get_settings()

    return MaintenanceService(
        policy=RetentionPolicy(
            content_days=settings.retention_content_days,
            audit_days=settings.retention_audit_days,
            backup_days=settings.retention_backup_days,
        ),
        backup_manager=create_backup_manager(),
    )
