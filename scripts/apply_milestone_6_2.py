from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
CONFIG_FILE = Path("src/tmb_ai_os/config.py")
FILES_TO_PATCH = (
    Path("src/tmb_ai_os/api_v18.py"),
    Path("src/tmb_ai_os/api_v19.py"),
)


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v21 import router as milestone_21_router\n"
    include_line = "app.include_router(milestone_21_router)\n"

    if import_line not in text:
        marker = "from .api_v20 import router as milestone_20_router\n"
        if marker not in text:
            raise SystemExit("Milestone 20 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_20_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 20 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")


def patch_config() -> None:
    text = CONFIG_FILE.read_text(encoding="utf-8")
    field = "    legacy_api_key_fallback_enabled: bool = True\n"
    marker = '    webhook_secret: str = ""\n'

    if field.strip() not in text:
        if marker not in text:
            raise SystemExit("Authentication settings marker was not found")
        text = text.replace(marker, marker + field)

    CONFIG_FILE.write_text(text, encoding="utf-8")


def patch_protected_apis() -> None:
    for path in FILES_TO_PATCH:
        text = path.read_text(encoding="utf-8")
        text = text.replace(
            "from .security_dependencies import permission_dependency\n",
            "from .unified_auth import unified_permission_dependency\n",
        )
        text = text.replace(
            "permission_dependency(",
            "unified_permission_dependency(",
        )
        path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_config()
    patch_protected_apis()
    print("Milestone 6.2 unified authentication added")


if __name__ == "__main__":
    main()
