from pathlib import Path

TARGETS = (
    Path("app/core/database.py"),
    Path("app/core/models.py"),
    Path("app/services/scheduler.py"),
)


def main() -> None:
    for path in TARGETS:
        backup = path.with_suffix(path.suffix + ".milestone4_3.bak")
        if not backup.exists():
            raise SystemExit(f"Missing backup: {backup}")

        path.write_text(
            backup.read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        print(f"Restored: {path}")


if __name__ == "__main__":
    main()
