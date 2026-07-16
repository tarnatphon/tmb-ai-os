import os

import uvicorn

from tmb_ai_os.config import get_settings
from tmb_ai_os.deployment import validate_deployment


def main() -> None:
    settings = get_settings()
    report = validate_deployment(settings)

    if not report.ready:
        for check in report.checks:
            if not check.passed:
                print(f"[FAIL] {check.name}: {check.detail}")
        raise SystemExit("Refusing to start with invalid production config")

    host = os.getenv("TMB_HOST", "0.0.0.0")
    port = int(os.getenv("TMB_PORT", "8000"))
    workers = int(os.getenv("TMB_WORKERS", "1"))

    uvicorn.run(
        "tmb_ai_os.main:app",
        host=host,
        port=port,
        workers=workers,
        reload=False,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )


if __name__ == "__main__":
    main()
