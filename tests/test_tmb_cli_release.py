from tools.tmb.commands.release import ReleaseReadiness, format_report
from tools.tmb.commands.version import VersionInfo


def version_info(synchronized: bool) -> VersionInfo:
    if synchronized:
        return VersionInfo(
            package_version="0.7.1",
            module_version="0.7.1",
            latest_tag="v0.7.1",
        )

    return VersionInfo(
        package_version="0.1.0",
        module_version="0.1.0",
        latest_tag="v0.7.1",
    )


def test_release_report_shows_ready_status() -> None:
    readiness = ReleaseReadiness(
        ready=True,
        reasons=(),
        version_info=version_info(synchronized=True),
    )

    report = format_report(readiness)

    assert "Status          : READY" in report
    assert "Reasons:" not in report


def test_release_report_shows_not_ready_reasons() -> None:
    readiness = ReleaseReadiness(
        ready=False,
        reasons=(
            "Git working tree is not clean",
            "Project version sources are out of sync",
        ),
        version_info=version_info(synchronized=False),
    )

    report = format_report(readiness)

    assert "Status          : NOT READY" in report
    assert "- Git working tree is not clean" in report
    assert "- Project version sources are out of sync" in report


def test_release_readiness_preserves_version_information() -> None:
    info = version_info(synchronized=False)
    readiness = ReleaseReadiness(
        ready=False,
        reasons=("Version mismatch",),
        version_info=info,
    )

    assert readiness.version_info is info
    assert readiness.ready is False
