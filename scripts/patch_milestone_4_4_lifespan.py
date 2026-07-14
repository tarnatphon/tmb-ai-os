from pathlib import Path

MAIN_FILE = Path("src/tmb_ai_os/main.py")


def main() -> None:
    text = MAIN_FILE.read_text(encoding="utf-8")

    import_line = "from .lifecycle import application_lifespan\n"
    if import_line not in text:
        marker = "from .api import app as api_app\n"
        if marker not in text:
            raise SystemExit("Could not find main import marker")
        text = text.replace(marker, marker + import_line)

    old_assignment = "app.router.lifespan_context = lifespan\n"
    new_assignment = "app.router.lifespan_context = application_lifespan\n"

    if old_assignment in text:
        text = text.replace(old_assignment, new_assignment)
    elif new_assignment not in text:
        marker = 'app.version = "0.4.0"\n'
        if marker not in text:
            raise SystemExit("Could not find lifespan assignment marker")
        text = text.replace(
            marker,
            marker + new_assignment,
        )

    MAIN_FILE.write_text(text, encoding="utf-8")
    print("Canonical application lifespan updated")


if __name__ == "__main__":
    main()
