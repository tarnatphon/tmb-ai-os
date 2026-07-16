from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")


def main() -> None:
    api_text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v20 import router as milestone_20_router\n"
    include_line = "app.include_router(milestone_20_router)\n"

    if import_line not in api_text:
        marker = "from .api_v19 import router as milestone_19_router\n"
        if marker not in api_text:
            raise SystemExit("Milestone 19 router import was not found")
        api_text = api_text.replace(marker, marker + import_line)

    if include_line not in api_text:
        marker = "app.include_router(milestone_19_router)\n"
        if marker not in api_text:
            raise SystemExit("Milestone 19 router registration was not found")
        api_text = api_text.replace(marker, marker + include_line)

    API_FILE.write_text(api_text, encoding="utf-8")

    database_text = DATABASE_FILE.read_text(encoding="utf-8")
    marker = "    from . import notification_models  # noqa: F401\n"
    addition = "    from . import api_key_models  # noqa: F401\n"

    if addition not in database_text:
        if marker not in database_text:
            raise SystemExit("API key model registration marker was not found")
        database_text = database_text.replace(
            marker,
            marker + addition,
        )

    DATABASE_FILE.write_text(
        database_text,
        encoding="utf-8",
    )
    print("Milestone 6.1 API key management added")


if __name__ == "__main__":
    main()
