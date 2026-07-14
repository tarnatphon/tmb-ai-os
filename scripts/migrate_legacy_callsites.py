import argparse
from pathlib import Path

from tmb_ai_os.migration.callsites import migrate_legacy_callsites


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate internal legacy imports to canonical modules."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report changes without writing files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    findings = migrate_legacy_callsites(
        Path.cwd(),
        write=not args.check,
    )

    if not findings:
        print("No legacy call sites found")
        return

    action = "Would migrate" if args.check else "Migrated"
    for finding in findings:
        relative = finding.file.relative_to(Path.cwd())
        print(
            f"{action}: {relative}:{finding.line} "
            f"{finding.legacy_module} -> "
            f"{finding.canonical_module}"
        )

    if args.check:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
