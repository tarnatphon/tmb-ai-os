import json
from dataclasses import asdict

from tmb_ai_os.backup_factory import create_backup_manager


def main() -> None:
    print(
        json.dumps(
            asdict(create_backup_manager().create()),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
