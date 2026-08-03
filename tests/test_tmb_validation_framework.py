from tools.tmb.validation import (
    ValidationResult,
    ValidationSummary,
    run_checks,
)


class PassingCheck:
    def run(self) -> ValidationResult:
        return ValidationResult(
            name="passing-check",
            passed=True,
            message="Check passed.",
            severity="info",
        )


class FailingCheck:
    def run(self) -> ValidationResult:
        return ValidationResult(
            name="failing-check",
            passed=False,
            message="Check failed.",
        )


def test_validation_result_defaults_to_error_severity() -> None:
    result = ValidationResult(
        name="example",
        passed=False,
        message="Failure.",
    )

    assert result.severity == "error"


def test_empty_validation_summary_passes() -> None:
    summary = ValidationSummary(results=())

    assert summary.passed is True
    assert summary.failed_count == 0


def test_run_checks_preserves_check_order() -> None:
    summary = run_checks([PassingCheck(), FailingCheck()])

    assert [result.name for result in summary.results] == [
        "passing-check",
        "failing-check",
    ]


def test_summary_fails_when_any_check_fails() -> None:
    summary = run_checks([PassingCheck(), FailingCheck()])

    assert summary.passed is False
    assert summary.failed_count == 1


def test_summary_passes_when_all_checks_pass() -> None:
    summary = run_checks([PassingCheck(), PassingCheck()])

    assert summary.passed is True
    assert summary.failed_count == 0
