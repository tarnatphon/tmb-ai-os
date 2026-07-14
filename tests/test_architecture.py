from pathlib import Path

from tmb_ai_os.architecture import inspect_architecture


def test_inspect_architecture_finds_duplicate_modules(
    tmp_path: Path,
) -> None:
    canonical = tmp_path / "src" / "tmb_ai_os"
    legacy = tmp_path / "app"
    canonical.mkdir(parents=True)
    legacy.mkdir()

    (canonical / "service.py").write_text("", encoding="utf-8")
    (legacy / "service.py").write_text("", encoding="utf-8")

    report = inspect_architecture(tmp_path)

    assert report.canonical_exists is True
    assert report.legacy_exists is True
    assert report.duplicate_modules == ("service",)
