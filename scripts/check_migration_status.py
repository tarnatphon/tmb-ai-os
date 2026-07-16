from tmb_ai_os.database import engine
from tmb_ai_os.migrations import get_migration_status


def main() -> None:
    status = get_migration_status(engine)

    print(f"Current revision: {status.current_revision}")
    print(f"Head revision:    {status.head_revision}")
    print(f"Up to date:       {status.up_to_date}")

    if not status.up_to_date:
        raise SystemExit("Database migration is not up to date")


if __name__ == "__main__":
    main()
