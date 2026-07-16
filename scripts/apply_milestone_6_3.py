from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
DATABASE_FILE = Path("src/tmb_ai_os/database.py")
PROTECTED_FILES = (
    Path("src/tmb_ai_os/api_v18.py"),
    Path("src/tmb_ai_os/api_v19.py"),
)


def patch_router() -> None:
    api_text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v22 import router as milestone_22_router\n"
    include_line = "app.include_router(milestone_22_router)\n"

    if import_line not in api_text:
        marker = "from .api_v21 import router as milestone_21_router\n"
        if marker not in api_text:
            raise SystemExit("Milestone 21 router import was not found")
        api_text = api_text.replace(marker, marker + import_line)

    if include_line not in api_text:
        marker = "app.include_router(milestone_21_router)\n"
        if marker not in api_text:
            raise SystemExit("Milestone 21 router registration was not found")
        api_text = api_text.replace(marker, marker + include_line)

    API_FILE.write_text(api_text, encoding="utf-8")


def patch_database() -> None:
    database_text = DATABASE_FILE.read_text(encoding="utf-8")
    marker = "    from . import api_key_models  # noqa: F401\n"
    addition = "    from . import api_key_scope_models  # noqa: F401\n"

    if addition not in database_text:
        if marker not in database_text:
            raise SystemExit("API key model registration marker was not found")
        database_text = database_text.replace(
            marker,
            marker + addition,
        )

    DATABASE_FILE.write_text(database_text, encoding="utf-8")


def patch_protected_routes() -> None:
    replacements = {
        Path("src/tmb_ai_os/api_v18.py"): ("ApiScope.DASHBOARD_READ"),
        Path("src/tmb_ai_os/api_v19.py"): ("ApiScope.SECURITY_ADMIN"),
    }

    for path, scope in replacements.items():
        text = path.read_text(encoding="utf-8")

        text = text.replace(
            "from .unified_auth import unified_permission_dependency\n",
            "from .scoped_auth import scope_dependency\nfrom .scopes import ApiScope\n",
        )
        text = text.replace(
            "unified_permission_dependency(Permission.SECURITY_ADMIN)",
            f"scope_dependency({scope})",
        )
        text = text.replace(
            "from .security import Permission, Principal\n",
            "from .security import Principal\n",
        )

        path.write_text(text, encoding="utf-8")


def main() -> None:
    patch_router()
    patch_database()
    patch_protected_routes()
    print("Milestone 6.3 scoped API keys added")


if __name__ == "__main__":
    main()
