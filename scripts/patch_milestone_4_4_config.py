from pathlib import Path

CONFIG_FILE = Path("src/tmb_ai_os/config.py")

FIELDS = (
    '    database_url: str = "sqlite:///data/tmb_ai_os.db"\n',
    '    app_timezone: str = "Asia/Bangkok"\n',
    "    scheduler_enabled: bool = False\n",
    "    scheduler_hour: int = 8\n",
    "    scheduler_minute: int = 0\n",
)


def main() -> None:
    text = CONFIG_FILE.read_text(encoding="utf-8")
    missing = [field for field in FIELDS if field.strip() not in text]

    if not missing:
        print("Milestone 4.4 settings already exist")
        return

    marker = '    ai_provider: str = "gemini"\n'
    if marker not in text:
        marker = '    env: str = "development"\n'

    if marker not in text:
        raise SystemExit("Could not find Settings insertion marker")

    addition = "".join(missing)
    CONFIG_FILE.write_text(
        text.replace(marker, marker + addition),
        encoding="utf-8",
    )
    print("Added database and scheduler settings")


if __name__ == "__main__":
    main()
