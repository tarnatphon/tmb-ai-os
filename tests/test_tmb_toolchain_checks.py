from tools.tmb.checks.toolchain import REQUIRED_TOOLS, ToolchainCheck


def all_tools_available(name: str) -> str:
    return f"/virtual/bin/{name}"


def test_toolchain_check_passes_when_all_tools_exist() -> None:
    result = ToolchainCheck(finder=all_tools_available).run()

    assert result.passed is True
    assert result.severity == "info"
    assert result.message == "Development toolchain is ready."


def test_toolchain_check_detects_one_missing_tool() -> None:
    check = ToolchainCheck(
        finder=lambda name: None if name == "ruff" else f"/bin/{name}",
    )

    result = check.run()

    assert result.passed is False
    assert result.message == "Missing development tools: ruff"


def test_toolchain_check_detects_multiple_missing_tools() -> None:
    missing = {"mypy", "pytest"}
    check = ToolchainCheck(
        finder=lambda name: None if name in missing else f"/bin/{name}",
    )

    result = check.run()

    assert result.passed is False
    assert result.message == "Missing development tools: mypy, pytest"


def test_toolchain_check_detects_all_missing_tools() -> None:
    result = ToolchainCheck(finder=lambda name: None).run()

    assert result.passed is False
    assert result.message == ("Missing development tools: " + ", ".join(REQUIRED_TOOLS))


def test_toolchain_check_reports_missing_tools_deterministically() -> None:
    check = ToolchainCheck(
        finder=lambda name: None if name in {"ruff", "git"} else "/bin/tool",
    )

    result = check.run()

    assert result.message == "Missing development tools: git, ruff"
