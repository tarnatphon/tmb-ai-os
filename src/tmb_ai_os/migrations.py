from dataclasses import dataclass
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Engine

from alembic import command


@dataclass(frozen=True)
class MigrationStatus:
    current_revision: str | None
    head_revision: str | None
    up_to_date: bool


def build_alembic_config(
    config_path: Path = Path("alembic.ini"),
) -> Config:
    config = Config(str(config_path))
    config.set_main_option("script_location", "alembic")
    return config


def get_migration_status(
    engine: Engine,
    config_path: Path = Path("alembic.ini"),
) -> MigrationStatus:
    config = build_alembic_config(config_path)
    head = ScriptDirectory.from_config(config).get_current_head()

    with engine.connect() as connection:
        current = MigrationContext.configure(connection).get_current_revision()

    return MigrationStatus(
        current_revision=current,
        head_revision=head,
        up_to_date=current == head,
    )


def upgrade_to_head(
    config_path: Path = Path("alembic.ini"),
) -> None:
    command.upgrade(
        build_alembic_config(config_path),
        "head",
    )
