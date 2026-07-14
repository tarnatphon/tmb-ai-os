from pathlib import Path

WRAPPERS: dict[Path, str] = {
    Path("app/core/database.py"): (
        "from tmb_ai_os.database import (\\n"
        "    Base,\\n"
        "    SessionLocal,\\n"
        "    engine,\\n"
        "    get_db,\\n"
        "    initialize_database,\\n"
        ")\\n\\n"
        "__all__ = [\\n"
        '    "Base",\\n'
        '    "SessionLocal",\\n'
        '    "engine",\\n'
        '    "get_db",\\n'
        '    "initialize_database",\\n'
        "]\\n"
    ),
    Path("app/core/models.py"): (
        'from tmb_ai_os.models import ContentRun\\n\\n__all__ = ["ContentRun"]\\n'
    ),
    Path("app/services/scheduler.py"): (
        "from tmb_ai_os.scheduler import (\\n"
        "    get_scheduler_state,\\n"
        "    scheduler,\\n"
        "    start_scheduler,\\n"
        "    stop_scheduler,\\n"
        ")\\n\\n"
        "__all__ = [\\n"
        '    "get_scheduler_state",\\n'
        '    "scheduler",\\n'
        '    "start_scheduler",\\n'
        '    "stop_scheduler",\\n'
        "]\\n"
    ),
}


def main() -> None:
    for path, wrapper in WRAPPERS.items():
        if not path.exists():
            raise SystemExit(f"Missing expected legacy file: {path}")

        backup = path.with_suffix(path.suffix + ".milestone4_3.bak")
        current = path.read_text(encoding="utf-8")

        if not backup.exists():
            backup.write_text(current, encoding="utf-8")

        path.write_text(wrapper, encoding="utf-8")
        print(f"Migrated: {path}")
        print(f"Backup:   {backup}")

    print("Milestone 4.4 database/model/scheduler migration applied")


if __name__ == "__main__":
    main()
