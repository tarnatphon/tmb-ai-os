import sqlite3
from pathlib import Path

from tmb_ai_os.backups import BackupManager


def test_backup_create_and_verify(tmp_path: Path) -> None:
    database_path = tmp_path / "data" / "app.db"
    database_path.parent.mkdir()
    with sqlite3.connect(database_path) as connection:
        connection.execute("create table example (id integer primary key)")

    content_dir = tmp_path / "content"
    knowledge_dir = tmp_path / "knowledge"
    content_dir.mkdir()
    knowledge_dir.mkdir()
    (content_dir / "a.md").write_text("a", encoding="utf-8")
    (knowledge_dir / "b.md").write_text("b", encoding="utf-8")

    manager = BackupManager(
        backup_dir=tmp_path / "backups",
        database_path=database_path,
        content_dir=content_dir,
        knowledge_dir=knowledge_dir,
    )
    manifest = manager.create()
    verified = manager.verify(manifest.name)

    assert verified.database_file is not None
    assert verified.archive_file is not None
