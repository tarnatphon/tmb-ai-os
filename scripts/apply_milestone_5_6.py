from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
CONFIG_FILE = Path("src/tmb_ai_os/config.py")


def main() -> None:
    api_text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v15 import router as milestone_15_router\n"
    include_line = "app.include_router(milestone_15_router)\n"

    if import_line not in api_text:
        marker = "from .api_v14 import router as milestone_14_router\n"
        if marker not in api_text:
            raise SystemExit("Milestone 14 router import was not found")
        api_text = api_text.replace(marker, marker + import_line)

    if include_line not in api_text:
        marker = "app.include_router(milestone_14_router)\n"
        if marker not in api_text:
            raise SystemExit("Milestone 14 router registration was not found")
        api_text = api_text.replace(marker, marker + include_line)

    API_FILE.write_text(api_text, encoding="utf-8")

    config_text = CONFIG_FILE.read_text(encoding="utf-8")
    marker = '    backup_dir: str = "backups"\n'
    fields = (
        "    retention_content_days: int = 365\n",
        "    retention_audit_days: int = 180\n",
        "    retention_backup_days: int = 90\n",
    )

    if marker not in config_text:
        raise SystemExit("Retention settings marker was not found")

    addition = "".join(field for field in fields if field.strip() not in config_text)
    if addition:
        config_text = config_text.replace(
            marker,
            marker + addition,
        )

    CONFIG_FILE.write_text(config_text, encoding="utf-8")
    print("Milestone 5.6 retention and maintenance added")


if __name__ == "__main__":
    main()
