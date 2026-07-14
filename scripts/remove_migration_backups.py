import argparse
from pathlib import Path

BACKUPS = (
    Path("app/core/config.py.milestone4_1.bak"),
    Path("app/providers/base.py.milestone4_1.bak"),
    Path("app/providers/factory.py.milestone4_1.bak"),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Remove committed migration backup files.")
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Actually remove backup files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    existing = [path for path in BACKUPS if path.exists()]

    if not existing:
        print("No migration backup files found")
        return

    for path in existing:
        if args.apply:
            path.unlink()
            print(f"Removed: {path}")
        else:
            print(f"Would remove: {path}")

    if not args.apply:
        print("Run again with --apply after the migration is verified")


if __name__ == "__main__":
    main()
