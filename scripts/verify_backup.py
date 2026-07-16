import argparse
import json
from dataclasses import asdict

from tmb_ai_os.backup_factory import create_backup_manager


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("backup_name")
    args = parser.parse_args()

    print(
        json.dumps(
            asdict(create_backup_manager().verify(args.backup_name)),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
