from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ArchitectureReport:
    canonical_package: Path
    legacy_package: Path
    canonical_exists: bool
    legacy_exists: bool
    duplicate_modules: tuple[str, ...]


def inspect_architecture(root: Path) -> ArchitectureReport:
    canonical = root / "src" / "tmb_ai_os"
    legacy = root / "app"

    canonical_modules = _module_names(canonical)
    legacy_modules = _module_names(legacy)

    duplicates = tuple(sorted(canonical_modules & legacy_modules))

    return ArchitectureReport(
        canonical_package=canonical,
        legacy_package=legacy,
        canonical_exists=canonical.exists(),
        legacy_exists=legacy.exists(),
        duplicate_modules=duplicates,
    )


def _module_names(package_root: Path) -> set[str]:
    if not package_root.exists():
        return set()

    names: set[str] = set()
    for path in package_root.rglob("*.py"):
        if path.name == "__init__.py":
            continue
        names.add(path.stem)
    return names
