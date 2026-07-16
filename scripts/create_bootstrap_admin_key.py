import argparse
import json
from dataclasses import asdict

from tmb_ai_os.api_key_service import ApiKeyService
from tmb_ai_os.database import SessionLocal
from tmb_ai_os.security import Role


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--key-id",
        default="primary-admin",
    )
    args = parser.parse_args()

    with SessionLocal() as session:
        created = ApiKeyService().create(
            session,
            key_id=args.key_id,
            role=Role.ADMIN,
        )

    print(
        json.dumps(
            asdict(created),
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
