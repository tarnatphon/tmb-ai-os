from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
CONFIG_FILE = Path("src/tmb_ai_os/config.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v10 import router as milestone_10_router\n"
    include_line = "app.include_router(milestone_10_router)\n"

    if import_line not in text:
        marker = "from .api_v9 import router as milestone_9_router\n"
        if marker not in text:
            raise SystemExit("Milestone 9 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_9_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 9 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")


def patch_config() -> None:
    text = CONFIG_FILE.read_text(encoding="utf-8")

    fields = (
        '    api_key: str = "change-me"\n',
        '    api_role: str = "admin"\n',
    )

    marker = "    scheduler_minute: int = 0\n"
    if marker not in text:
        raise SystemExit("Settings insertion marker was not found")

    addition = "".join(field for field in fields if field.strip() not in text)
    if addition:
        text = text.replace(marker, marker + addition)

    CONFIG_FILE.write_text(text, encoding="utf-8")


def patch_database() -> None:
    text = DATABASE_FILE.read_text(encoding="utf-8")
    marker = "    from . import audit_models  # noqa: F401\n"
    addition = "    from . import security_models  # noqa: F401\n"

    if addition not in text:
        if marker not in text:
            raise SystemExit("Database model registration marker was not found")
        text = text.replace(marker, marker + addition)

    DATABASE_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_config()
    patch_database()
    print("Milestone 5.1 security and RBAC added")


if __name__ == "__main__":
    main()
