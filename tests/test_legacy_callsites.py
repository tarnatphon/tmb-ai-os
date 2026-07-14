from pathlib import Path

from tmb_ai_os.migration.callsites import (
    find_legacy_callsites,
    migrate_legacy_callsites,
)


def test_migration_rewrites_known_legacy_imports(
    tmp_path: Path,
) -> None:
    app_dir = tmp_path / "app" / "services"
    app_dir.mkdir(parents=True)

    target = app_dir / "example.py"
    target.write_text(
        "from app.core.config import settings\nfrom app.providers.base import GenerationRequest\n",
        encoding="utf-8",
    )

    findings = migrate_legacy_callsites(tmp_path, write=True)
    updated = target.read_text(encoding="utf-8")

    assert len(findings) == 2
    assert "from tmb_ai_os.config import settings" in updated
    assert ("from tmb_ai_os.provider_contracts import GenerationRequest") in updated


def test_current_project_has_no_internal_legacy_callsites() -> None:
    findings = find_legacy_callsites(Path.cwd())

    assert findings == ()
