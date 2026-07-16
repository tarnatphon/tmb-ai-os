from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
CONFIG_FILE = Path("src/tmb_ai_os/config.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")


def main() -> None:
    api_text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v17 import router as milestone_17_router\n"
    include_line = "app.include_router(milestone_17_router)\n"

    if import_line not in api_text:
        marker = "from .api_v16 import router as milestone_16_router\n"
        if marker not in api_text:
            raise SystemExit("Milestone 16 router import was not found")
        api_text = api_text.replace(marker, marker + import_line)

    if include_line not in api_text:
        marker = "app.include_router(milestone_16_router)\n"
        if marker not in api_text:
            raise SystemExit("Milestone 16 router registration was not found")
        api_text = api_text.replace(marker, marker + include_line)

    API_FILE.write_text(api_text, encoding="utf-8")

    config_text = CONFIG_FILE.read_text(encoding="utf-8")
    marker = "    retention_backup_days: int = 90\n"
    fields = (
        '    notification_provider: str = "dry_run"\n',
        '    webhook_url: str = ""\n',
        '    webhook_secret: str = ""\n',
    )
    if marker not in config_text:
        raise SystemExit("Notification settings marker was not found")

    addition = "".join(field for field in fields if field.strip() not in config_text)
    if addition:
        config_text = config_text.replace(
            marker,
            marker + addition,
        )

    CONFIG_FILE.write_text(config_text, encoding="utf-8")

    database_text = DATABASE_FILE.read_text(encoding="utf-8")
    marker = "    from . import incident_models  # noqa: F401\n"
    addition = "    from . import notification_models  # noqa: F401\n"

    if addition not in database_text:
        if marker not in database_text:
            raise SystemExit("Notification model registration marker was not found")
        database_text = database_text.replace(
            marker,
            marker + addition,
        )

    DATABASE_FILE.write_text(database_text, encoding="utf-8")
    print("Milestone 5.8 webhook notifications added")


if __name__ == "__main__":
    main()
