from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
CONFIG_FILE = Path("src/tmb_ai_os/config.py")


def main() -> None:
    api_text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v14 import router as milestone_14_router\n"
    include_line = "app.include_router(milestone_14_router)\n"

    if import_line not in api_text:
        marker = "from .api_v13 import router as milestone_13_router\n"
        if marker not in api_text:
            raise SystemExit("Milestone 13 router import was not found")
        api_text = api_text.replace(marker, marker + import_line)

    if include_line not in api_text:
        marker = "app.include_router(milestone_13_router)\n"
        if marker not in api_text:
            raise SystemExit("Milestone 13 router registration was not found")
        api_text = api_text.replace(marker, marker + include_line)

    API_FILE.write_text(api_text, encoding="utf-8")

    config_text = CONFIG_FILE.read_text(encoding="utf-8")
    field = '    backup_dir: str = "backups"\n'
    marker = "    rate_limit_window_seconds: int = 60\n"
    if field.strip() not in config_text:
        if marker not in config_text:
            raise SystemExit("Backup settings marker was not found")
        config_text = config_text.replace(marker, marker + field)

    CONFIG_FILE.write_text(config_text, encoding="utf-8")
    print("Milestone 5.5 backup and recovery added")


if __name__ == "__main__":
    main()
