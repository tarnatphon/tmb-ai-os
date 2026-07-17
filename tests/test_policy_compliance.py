from tmb_ai_os.main import app
from tmb_ai_os.policy_compliance import (
    build_policy_compliance_report,
)


def test_policy_compliance_report_is_created() -> None:
    report = build_policy_compliance_report(app)

    assert report.protected_routes >= report.covered_routes
