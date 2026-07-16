from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
DASHBOARD_API_FILE = Path("src/tmb_ai_os/api_v18.py")


def patch_api() -> None:
    text = API_FILE.read_text(encoding="utf-8")

    import_line = "from .api_v19 import router as milestone_19_router\n"
    include_line = "app.include_router(milestone_19_router)\n"

    if import_line not in text:
        marker = "from .api_v18 import router as milestone_18_router\n"
        if marker not in text:
            raise SystemExit("Milestone 18 router import was not found")
        text = text.replace(marker, marker + import_line)

    if include_line not in text:
        marker = "app.include_router(milestone_18_router)\n"
        if marker not in text:
            raise SystemExit("Milestone 18 router registration was not found")
        text = text.replace(marker, marker + include_line)

    API_FILE.write_text(text, encoding="utf-8")


def patch_dashboard_api() -> None:
    text = DASHBOARD_API_FILE.read_text(encoding="utf-8")

    security_import = (
        "from .security import Permission, Principal\n"
        "from .security_dependencies import permission_dependency\n"
    )
    if security_import not in text:
        marker = "from .database import get_db\n"
        if marker not in text:
            raise SystemExit("Dashboard dependency marker was not found")
        text = text.replace(
            marker,
            marker + security_import,
        )

    alias = (
        "AdminPrincipal = Annotated[\n"
        "    Principal,\n"
        "    Depends(permission_dependency(Permission.SECURITY_ADMIN)),\n"
        "]\n"
    )
    if alias not in text:
        marker = "DbSession = Annotated[Session, Depends(get_db)]\n"
        if marker not in text:
            raise SystemExit("Dashboard session alias marker was not found")
        text = text.replace(
            marker,
            marker + alias,
        )

    for signature in (
        "def dashboard_summary(\n    db: DbSession,\n",
        "def dashboard_incidents(\n    db: DbSession,\n",
        "def dashboard_notifications(\n    db: DbSession,\n",
    ):
        replacement = signature.replace(
            "    db: DbSession,\n",
            "    _: AdminPrincipal,\n    db: DbSession,\n",
        )
        if signature in text and replacement not in text:
            text = text.replace(signature, replacement)

    DASHBOARD_API_FILE.write_text(text, encoding="utf-8")


def main() -> None:
    patch_api()
    patch_dashboard_api()
    print("Milestone 6.0 secure admin dashboard added")


if __name__ == "__main__":
    main()
