from pathlib import Path

CONFIG_FILE = Path("src/tmb_ai_os/config.py")


def main() -> None:
    text = CONFIG_FILE.read_text(encoding="utf-8")

    if "ai_provider:" in text:
        print("ai_provider already exists")
        return

    marker = '    env: str = "development"\n'
    addition = '    ai_provider: str = "gemini"\n'

    if marker not in text:
        raise SystemExit("Could not find Settings.env insertion marker")

    CONFIG_FILE.write_text(
        text.replace(marker, marker + addition),
        encoding="utf-8",
    )
    print("Added Settings.ai_provider")


if __name__ == "__main__":
    main()
