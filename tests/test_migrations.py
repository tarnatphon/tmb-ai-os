from pathlib import Path

from tmb_ai_os.migrations import build_alembic_config


def test_build_alembic_config() -> None:
    config = build_alembic_config(Path("alembic.ini"))

    assert config.get_main_option("script_location") == "alembic"
