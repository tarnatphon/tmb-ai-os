from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from tmb_ai_os.database import (
    Base,
    build_engine,
    ensure_sqlite_parent,
)


def test_build_engine_supports_in_memory_sqlite() -> None:
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        result = session.execute(text("select 1")).scalar_one()

    assert result == 1


def test_ensure_sqlite_parent_creates_directory(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "nested" / "database.db"

    ensure_sqlite_parent(f"sqlite:///{database_path}")

    assert database_path.parent.exists()
