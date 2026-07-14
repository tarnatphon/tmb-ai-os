from dataclasses import dataclass
from enum import StrEnum


class MigrationStatus(StrEnum):
    PENDING = "pending"
    WRAPPED = "wrapped"
    MIGRATED = "migrated"
    REMOVED = "removed"


@dataclass(frozen=True)
class MigrationItem:
    legacy_module: str
    canonical_module: str
    status: MigrationStatus
    notes: str


MIGRATION_MANIFEST: tuple[MigrationItem, ...] = (
    MigrationItem(
        legacy_module="app.core.config",
        canonical_module="tmb_ai_os.config",
        status=MigrationStatus.PENDING,
        notes="Compare settings names and environment variable contracts.",
    ),
    MigrationItem(
        legacy_module="app.providers.base",
        canonical_module="tmb_ai_os.providers",
        status=MigrationStatus.PENDING,
        notes="Preserve provider protocol and response contracts.",
    ),
    MigrationItem(
        legacy_module="app.providers.factory",
        canonical_module="tmb_ai_os.providers",
        status=MigrationStatus.PENDING,
        notes="Map legacy provider selection to canonical generator factory.",
    ),
    MigrationItem(
        legacy_module="app.main",
        canonical_module="tmb_ai_os.main",
        status=MigrationStatus.WRAPPED,
        notes="Legacy entry point delegates to canonical FastAPI app.",
    ),
)
