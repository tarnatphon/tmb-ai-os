import json
from dataclasses import asdict

from tmb_ai_os.database import SessionLocal
from tmb_ai_os.maintenance_factory import create_maintenance_service


def main() -> None:
    with SessionLocal() as session:
        preview = create_maintenance_service().preview(session)

    print(
        json.dumps(
            asdict(preview),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
