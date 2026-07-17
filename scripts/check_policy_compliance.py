from tmb_ai_os.main import app
from tmb_ai_os.policy_compliance import (
    build_policy_compliance_report,
)


def main() -> None:
    report = build_policy_compliance_report(app)
    if report.gaps:
        raise SystemExit(
            "Missing scope policies:\n"
            + "\n".join(f"{gap.method} {gap.path}" for gap in report.gaps)
        )
    print("Authorization policy compliance passed")


if __name__ == "__main__":
    main()
