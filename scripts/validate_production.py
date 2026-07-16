from tmb_ai_os.config import get_settings
from tmb_ai_os.deployment import validate_deployment


def main() -> None:
    report = validate_deployment(get_settings())

    for check in report.checks:
        state = "PASS" if check.passed else "FAIL"
        print(f"[{state}] {check.name}: {check.detail}")

    if not report.ready:
        raise SystemExit("Production validation failed")

    print("Production validation passed")


if __name__ == "__main__":
    main()
