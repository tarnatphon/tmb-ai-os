from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")


def main() -> None:
    if not API_FILE.exists():
        raise SystemExit(f"Missing expected file: {API_FILE}")

    text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v4 import router as milestone_4_router\n"
    include_line = "app.include_router(milestone_4_router)\n"

    if import_line not in text:
        marker = "from .api_v3 import router as milestone_3_router\n"
        if marker not in text:
            raise SystemExit("Milestone 3 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_3_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 3 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")
    print("Milestone 4.5 router added to src/tmb_ai_os/api.py")


if __name__ == "__main__":
    main()
