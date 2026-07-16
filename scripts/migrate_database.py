from tmb_ai_os.migrations import upgrade_to_head


def main() -> None:
    upgrade_to_head()
    print("Database migrated to Alembic head")


if __name__ == "__main__":
    main()
