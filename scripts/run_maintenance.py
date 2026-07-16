import argparse
import json
from dataclasses import asdict

from tmb_ai_os.database import SessionLocal
from tmb_ai_os.maintenance_factory import create_maintenance_service


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--confirm",
        action="store_true",
    )
    args = parser.parse_args()

    with SessionLocal() as session:
        result = create_maintenance_service().run(
            session,
            confirm=args.confirm,
        )

    print(
        json.dumps(
            asdict(result),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
