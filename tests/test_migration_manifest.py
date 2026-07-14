from tmb_ai_os.migration.manifest import (
    MIGRATION_MANIFEST,
    MigrationStatus,
)


def test_manifest_contains_main_compatibility_wrapper() -> None:
    main_item = next(item for item in MIGRATION_MANIFEST if item.legacy_module == "app.main")

    assert main_item.status is MigrationStatus.WRAPPED
    assert main_item.canonical_module == "tmb_ai_os.main"
