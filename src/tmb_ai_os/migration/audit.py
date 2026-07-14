import ast
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class DependencyFinding:
    file: str
    line: int
    imported_module: str
    direction: str


@dataclass(frozen=True)
class DependencyReport:
    root: str
    findings: tuple[DependencyFinding, ...]

    @property
    def canonical_to_legacy(self) -> tuple[DependencyFinding, ...]:
        return tuple(
            finding for finding in self.findings if finding.direction == "canonical_to_legacy"
        )

    @property
    def legacy_to_canonical(self) -> tuple[DependencyFinding, ...]:
        return tuple(
            finding for finding in self.findings if finding.direction == "legacy_to_canonical"
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "root": self.root,
            "summary": {
                "total": len(self.findings),
                "canonical_to_legacy": len(self.canonical_to_legacy),
                "legacy_to_canonical": len(self.legacy_to_canonical),
            },
            "findings": [asdict(finding) for finding in self.findings],
        }


def audit_dependencies(root: Path) -> DependencyReport:
    findings: list[DependencyFinding] = []

    canonical_root = root / "src" / "tmb_ai_os"
    legacy_root = root / "app"

    for file_path, source_package, target_package, direction in (
        (
            canonical_root,
            "tmb_ai_os",
            "app",
            "canonical_to_legacy",
        ),
        (
            legacy_root,
            "app",
            "tmb_ai_os",
            "legacy_to_canonical",
        ),
    ):
        if not file_path.exists():
            continue

        for python_file in sorted(file_path.rglob("*.py")):
            findings.extend(
                _scan_file(
                    python_file=python_file,
                    project_root=root,
                    source_package=source_package,
                    target_package=target_package,
                    direction=direction,
                )
            )

    return DependencyReport(
        root=str(root.resolve()),
        findings=tuple(findings),
    )


def _scan_file(
    python_file: Path,
    project_root: Path,
    source_package: str,
    target_package: str,
    direction: str,
) -> list[DependencyFinding]:
    del source_package

    try:
        tree = ast.parse(
            python_file.read_text(encoding="utf-8"),
            filename=str(python_file),
        )
    except (OSError, SyntaxError):
        return []

    findings: list[DependencyFinding] = []
    for node in ast.walk(tree):
        imported_modules = _imported_modules(node)
        for imported_module in imported_modules:
            if imported_module == target_package or imported_module.startswith(
                f"{target_package}."
            ):
                findings.append(
                    DependencyFinding(
                        file=str(python_file.relative_to(project_root)),
                        line=getattr(node, "lineno", 0),
                        imported_module=imported_module,
                        direction=direction,
                    )
                )

    return findings


def _imported_modules(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)

    if isinstance(node, ast.ImportFrom):
        if node.module is None:
            return ()
        return (node.module,)

    return ()
