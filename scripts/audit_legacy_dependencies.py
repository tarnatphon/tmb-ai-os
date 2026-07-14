import argparse
import json
from pathlib import Path

from tmb_ai_os.migration import audit_dependencies
from tmb_ai_os.migration.manifest import MIGRATION_MANIFEST


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit dependencies between app and tmb_ai_os packages."
    )
    parser.add_argument(
        "--json",
        type=Path,
        dest="json_path",
        help="Optional JSON report output path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = audit_dependencies(Path.cwd())

    print("Legacy dependency audit")
    print(f"Total findings: {len(report.findings)}")
    print(f"Canonical -> legacy: {len(report.canonical_to_legacy)}")
    print(f"Legacy -> canonical: {len(report.legacy_to_canonical)}")

    if report.findings:
        print("\nFindings:")
        for finding in report.findings:
            print(
                f"- {finding.direction}: {finding.file}:{finding.line} -> {finding.imported_module}"
            )

    print("\nMigration manifest:")
    for item in MIGRATION_MANIFEST:
        print(f"- {item.status.value}: {item.legacy_module} -> {item.canonical_module}")

    if args.json_path is not None:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(
            json.dumps(
                report.to_dict(),
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nJSON report written: {args.json_path}")


if __name__ == "__main__":
    main()
