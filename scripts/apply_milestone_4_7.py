from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v6 import router as milestone_6_router\n"
    include_line = "app.include_router(milestone_6_router)\n"

    if import_line not in text:
        marker = "from .api_v5 import router as milestone_5_router\n"
        if marker not in text:
            raise SystemExit("Milestone 5 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_5_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 5 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")


def patch_database_registration() -> None:
    text = DATABASE_FILE.read_text(encoding="utf-8")

    marker = "    from . import models  # noqa: F401\n"
    addition = "    from . import audit_models  # noqa: F401\n"

    if addition not in text:
        if marker not in text:
            raise SystemExit("Database model registration marker was not found")
        text = text.replace(marker, marker + addition)

    DATABASE_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_database_registration()
    print("Milestone 4.7 approval workflow added")


if __name__ == "__main__":
    main()
