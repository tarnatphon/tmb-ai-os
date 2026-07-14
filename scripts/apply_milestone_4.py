from pathlib import Path

LEGACY_MAIN = Path("app/main.py")
BACKUP_MAIN = Path("app/main.py.milestone3.bak")


def main() -> None:
    if not LEGACY_MAIN.exists():
        raise SystemExit("Missing app/main.py")

    current = LEGACY_MAIN.read_text(encoding="utf-8")

    if "from tmb_ai_os.main import app" in current:
        print("Milestone 4 compatibility layer already applied")
        return

    if not BACKUP_MAIN.exists():
        BACKUP_MAIN.write_text(current, encoding="utf-8")

    LEGACY_MAIN.write_text(
        'from tmb_ai_os.main import app\n\n__all__ = ["app"]\n',
        encoding="utf-8",
    )

    print("Architecture unification applied")
    print(f"Legacy backup: {BACKUP_MAIN}")
    print("Canonical entry point: tmb_ai_os.main:app")


if __name__ == "__main__":
    main()
