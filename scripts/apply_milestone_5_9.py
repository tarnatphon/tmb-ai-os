from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")


def main() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    api_import = "from .api_v18 import router as milestone_18_router\n"
    admin_import = "from .admin_dashboard import router as admin_dashboard_router\n"
    api_include = "app.include_router(milestone_18_router)\n"
    admin_include = "app.include_router(admin_dashboard_router)\n"

    if api_import not in text:
        marker = "from .api_v17 import router as milestone_17_router\n"
        if marker not in text:
            raise SystemExit("Milestone 17 router import was not found")
        text = text.replace(
            marker,
            marker + api_import + admin_import,
        )

    if api_include not in text:
        marker = "app.include_router(milestone_17_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 17 router registration was not found")
        text = text.replace(
            marker,
            marker + api_include + admin_include,
        )

    API_FILE.write_text(text, encoding="utf-8")
    print("Milestone 5.9 operations dashboard added")


if __name__ == "__main__":
    main()
