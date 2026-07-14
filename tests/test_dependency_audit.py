from pathlib import Path

from tmb_ai_os.migration import audit_dependencies


def test_audit_detects_canonical_to_legacy_import(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "src" / "tmb_ai_os"
    legacy = tmp_path / "app"
    canonical.mkdir(parents=True)
    legacy.mkdir()

    (canonical / "bad.py").write_text(
        "from app.core.config import settings\n",
        encoding="utf-8",
    )
    (legacy / "main.py").write_text(
        "from tmb_ai_os.main import app\n",
        encoding="utf-8",
    )

    report = audit_dependencies(tmp_path)

    assert len(report.canonical_to_legacy) == 1
    assert len(report.legacy_to_canonical) == 1
    assert report.canonical_to_legacy[0].imported_module == "app.core.config"


def test_current_canonical_package_has_no_legacy_imports() -> None:
    report = audit_dependencies(Path.cwd())

    assert report.canonical_to_legacy == ()
