from pathlib import Path

API_FILE = Path("src/tmb_ai_os/api.py")
PYPROJECT_FILE = Path("pyproject.toml")


def main() -> None:
    api_text = API_FILE.read_text(encoding="utf-8")
    import_line = "from .api_v13 import router as milestone_13_router\n"
    include_line = "app.include_router(milestone_13_router)\n"

    if import_line not in api_text:
        marker = "from .api_v12 import router as milestone_12_router\n"
        if marker not in api_text:
            raise SystemExit("Milestone 12 router import was not found")
        api_text = api_text.replace(marker, marker + import_line)

    if include_line not in api_text:
        marker = "app.include_router(milestone_12_router)\n"
        if marker not in api_text:
            raise SystemExit("Milestone 12 router registration was not found")
        api_text = api_text.replace(marker, marker + include_line)

    API_FILE.write_text(api_text, encoding="utf-8")

    project_text = PYPROJECT_FILE.read_text(encoding="utf-8")
    marker = "dependencies = [\n"
    for dependency in reversed(
        (
            '  "alembic>=1.14,<2",\n',
            '  "psycopg[binary]>=3.2,<4",\n',
        )
    ):
        package = dependency.split('"')[1].split(">=")[0]
        if package not in project_text:
            project_text = project_text.replace(
                marker,
                marker + dependency,
            )

    PYPROJECT_FILE.write_text(project_text, encoding="utf-8")
    print("Milestone 5.4 Alembic and PostgreSQL readiness added")


if __name__ == "__main__":
    main()
