from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
TARGETS = (
    Path("src/tmb_ai_os/api_v4.py"),
    Path("src/tmb_ai_os/api_v16.py"),
    Path("src/tmb_ai_os/api_v17.py"),
    Path("src/tmb_ai_os/api_v20.py"),
)


def patch_router() -> None:
    text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v23 import router as milestone_23_router\n"
    include_line = "app.include_router(milestone_23_router)\n"

    if import_line not in text:
        marker = "from .api_v22 import router as milestone_22_router\n"
        if marker not in text:
            raise SystemExit("Milestone 22 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_22_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 22 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")


def patch_files() -> None:
    for path in TARGETS:
        text = path.read_text(encoding="utf-8")
        if "from .scoped_auth import scope_dependency\n" not in text:
            marker = "from .database import get_db\n"
            if marker not in text:
                raise SystemExit(f"Database import marker missing in {path}")
            text = text.replace(
                marker,
                marker
                + "from .scoped_auth import scope_dependency\n"
                + "from .scopes import ApiScope\n",
            )
        path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_router()
    patch_files()
    print("Milestone 6.4 scope enforcement added")


if __name__ == "__main__":
    main()
