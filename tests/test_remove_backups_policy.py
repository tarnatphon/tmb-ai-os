from pathlib import Path


def test_backup_removal_script_requires_apply_flag() -> None:
    script = Path("scripts/remove_migration_backups.py").read_text(encoding="utf-8")

    assert "--apply" in script
    assert "path.unlink()" in script
