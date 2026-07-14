from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")


def main() -> None:
    if not API_FILE.exists():
        raise SystemExit(f"Missing expected file: {API_FILE}")

    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v2 import router as milestone_2_router\n"
    include_line = "app.include_router(milestone_2_router)\n"

    if import_line not in text:
        marker = "from .config import get_settings\n"
        if marker not in text:
            raise SystemExit("Could not find API import insertion marker")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = 'app = FastAPI(title="TMB AI OS", version="0.1.0")\n'
        if marker not in text:
            raise SystemExit("Could not find FastAPI insertion marker")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")
    print("Milestone 2 router added to src/tmb_ai_os/api.py")


if __name__ == "__main__":
    main()
