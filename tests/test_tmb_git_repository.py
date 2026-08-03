from __future__ import annotations

import subprocess
from pathlib import Path

from tools.tmb.checks.git_repository import GitRepositoryCheck


class FakeGitRunner:
    def __init__(
        self,
        responses: dict[tuple[str, ...], tuple[int, str]],
    ) -> None:
        self.responses = responses

    def __call__(
        self,
        root: Path,
        arguments: tuple[str, ...],
    ) -> subprocess.CompletedProcess[str]:
        del root
        returncode, stdout = self.responses.get(arguments, (1, ""))
        return subprocess.CompletedProcess(
            args=("git", *arguments),
            returncode=returncode,
            stdout=stdout,
            stderr="",
        )


def valid_responses(
    status: str = "",
) -> dict[tuple[str, ...], tuple[int, str]]:
    return {
        ("rev-parse", "--show-toplevel"): (0, "/repo\n"),
        ("branch", "--show-current"): (0, "main\n"),
        ("remote", "get-url", "origin"): (0, "git@example/repo.git\n"),
        ("status", "--porcelain"): (0, status),
    }


def test_git_repository_check_passes_for_clean_repository(
    tmp_path: Path,
) -> None:
    check = GitRepositoryCheck(
        root=tmp_path,
        runner=FakeGitRunner(valid_responses()),
    )

    result = check.run()

    assert result.passed is True
    assert result.severity == "info"
    assert "branch main" in result.message
    assert "working tree clean" in result.message


def test_git_repository_check_allows_changes_by_default(
    tmp_path: Path,
) -> None:
    check = GitRepositoryCheck(
        root=tmp_path,
        runner=FakeGitRunner(valid_responses(" M file.py\n")),
    )

    result = check.run()

    assert result.passed is True
    assert "working tree has changes" in result.message


def test_git_repository_check_can_require_clean_tree(
    tmp_path: Path,
) -> None:
    check = GitRepositoryCheck(
        root=tmp_path,
        require_clean=True,
        runner=FakeGitRunner(valid_responses(" M file.py\n")),
    )

    result = check.run()

    assert result.passed is False
    assert "working tree is not clean" in result.message


def test_git_repository_check_rejects_non_repository(
    tmp_path: Path,
) -> None:
    check = GitRepositoryCheck(
        root=tmp_path,
        runner=FakeGitRunner({}),
    )

    result = check.run()

    assert result.passed is False
    assert "not a Git repository" in result.message


def test_git_repository_check_requires_current_branch(
    tmp_path: Path,
) -> None:
    responses = valid_responses()
    responses[("branch", "--show-current")] = (0, "")
    check = GitRepositoryCheck(
        root=tmp_path,
        runner=FakeGitRunner(responses),
    )

    result = check.run()

    assert result.passed is False
    assert "current Git branch" in result.message


def test_git_repository_check_requires_origin_remote(
    tmp_path: Path,
) -> None:
    responses = valid_responses()
    responses[("remote", "get-url", "origin")] = (1, "")
    check = GitRepositoryCheck(
        root=tmp_path,
        runner=FakeGitRunner(responses),
    )

    result = check.run()

    assert result.passed is False
    assert "origin remote" in result.message
