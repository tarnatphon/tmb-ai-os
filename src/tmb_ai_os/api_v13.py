from dataclasses import asdict

from fastapi import APIRouter

from .config import get_settings
from .database import engine
from .migrations import get_migration_status

router = APIRouter(prefix="/v13", tags=["Milestone 5.4"])


@router.get("/database/migration-status")
def migration_status() -> dict[str, object]:
    return asdict(get_migration_status(engine))


@router.get("/database/config")
def database_config() -> dict[str, object]:
    scheme = get_settings().database_url.split(":", maxsplit=1)[0]
    return {
        "scheme": scheme,
        "postgresql_ready": scheme.startswith("postgresql"),
        "sqlite": scheme == "sqlite",
    }
