import ast
from dataclasses import dataclass
from pathlib import Path

LEGACY_IMPORT_MAP: dict[str, str] = {
    "app.core.config": "tmb_ai_os.config",
    "app.providers.base": "tmb_ai_os.provider_contracts",
    "app.providers.factory": "tmb_ai_os.provider_factory",
}


@dataclass(frozen=True)
class LegacyCallSite:
    file: Path
    line: int
    legacy_module: str
    canonical_module: str


def find_legacy_callsites(root: Path) -> tuple[LegacyCallSite, ...]:
    findings: list[LegacyCallSite] = []

    for python_file in sorted(_iter_source_files(root)):
        if _is_excluded(python_file):
            continue

        try:
            tree = ast.parse(
                python_file.read_text(encoding="utf-8"),
                filename=str(python_file),
            )
        except (OSError, SyntaxError):
            continue

        for node in ast.walk(tree):
            imported_module = _module_from_node(node)
            if imported_module is None:
                continue

            canonical = LEGACY_IMPORT_MAP.get(imported_module)
            if canonical is None:
                continue

            findings.append(
                LegacyCallSite(
                    file=python_file,
                    line=getattr(node, "lineno", 0),
                    legacy_module=imported_module,
                    canonical_module=canonical,
                )
            )

    return tuple(findings)


def migrate_legacy_callsites(
    root: Path,
    *,
    write: bool,
) -> tuple[LegacyCallSite, ...]:
    findings = find_legacy_callsites(root)

    by_file: dict[Path, list[LegacyCallSite]] = {}
    for finding in findings:
        by_file.setdefault(finding.file, []).append(finding)

    if write:
        for file_path, file_findings in by_file.items():
            text = file_path.read_text(encoding="utf-8")
            for finding in file_findings:
                text = text.replace(
                    finding.legacy_module,
                    finding.canonical_module,
                )
            file_path.write_text(text, encoding="utf-8")

    return findings


def _iter_source_files(root: Path) -> list[Path]:
    roots = [
        root / "app",
        root / "src",
        root / "scripts",
        root / "tests",
    ]
    files: list[Path] = []
    for source_root in roots:
        if source_root.exists():
            files.extend(source_root.rglob("*.py"))
    return files


def _is_excluded(path: Path) -> bool:
    name = path.name
    if ".bak" in name:
        return True

    normalized = path.as_posix()
    excluded = (
        "app/core/config.py",
        "app/providers/base.py",
        "app/providers/factory.py",
        "scripts/migrate_legacy_callsites.py",
        "scripts/check_legacy_callsites.py",
    )
    return normalized.endswith(excluded)


def _module_from_node(node: ast.AST) -> str | None:
    if isinstance(node, ast.ImportFrom):
        return node.module

    if isinstance(node, ast.Import) and len(node.names) == 1:
        return node.names[0].name

    return None
