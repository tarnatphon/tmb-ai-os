import argparse
import json
from dataclasses import asdict

from tmb_ai_os.backup_factory import create_backup_manager


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("backup_name")
    parser.add_argument("--confirm", action="store_true")
    args = parser.parse_args()

    print(
        json.dumps(
            asdict(
                create_backup_manager().restore(
                    args.backup_name,
                    confirm=args.confirm,
                )
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
