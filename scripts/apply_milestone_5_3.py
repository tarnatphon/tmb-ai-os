from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")


def main() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v12 import router as milestone_12_router\n"
    include_line = "app.include_router(milestone_12_router)\n"

    if import_line not in text:
        marker = "from .api_v11 import router as milestone_11_router\n"
        if marker not in text:
            raise SystemExit("Milestone 11 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_11_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 11 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")
    print("Milestone 5.3 deployment endpoints added")


if __name__ == "__main__":
    main()
