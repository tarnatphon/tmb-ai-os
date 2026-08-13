from __future__ import annotations

import json
from pathlib import Path

from tools.patch_engine import PatchValidationError, TransactionError
from tools.patch_engine.cli import main
from tools.patch_engine.parser import parse_python_source
from tools.patch_engine.runner import run_command, run_validation_plan
from tools.patch_engine.transaction import FileReplacement, PatchTransaction
from tools.patch_engine.validator import (
    PythonStructureRequirement,
    validate_python_structure,
)

ROOT = Path(__file__).resolve().parents[1]


def test_parse_python_source_rejects_invalid_syntax() -> None:
    try:
        parse_python_source("def broken(:\n", path=Path("broken.py"))
    except PatchValidationError as exc:
        assert "invalid Python syntax" in str(exc)
    else:
        raise AssertionError("invalid syntax should fail validation")


def test_validate_python_structure_requires_top_level_symbols() -> None:
    module = parse_python_source(
        "class Service:\n    pass\n\n\ndef run() -> int:\n    return 0\n",
        path=Path("service.py"),
    )

    validate_python_structure(
        module,
        PythonStructureRequirement(
            functions=("run",),
            classes=("Service",),
        ),
    )


def test_transaction_restores_existing_file_when_write_fails(tmp_path: Path) -> None:
    target = tmp_path / "module.py"
    directory_target = tmp_path / "directory"
    target.write_text("original\n", encoding="utf-8")
    directory_target.mkdir()

    transaction = PatchTransaction()

    try:
        transaction.apply(
            (
                FileReplacement(path=target, content="changed\n"),
                FileReplacement(path=directory_target, content="cannot write here\n"),
            ),
        )
    except TransactionError:
        pass
    else:
        raise AssertionError("transaction should fail when a target is a directory")

    assert target.read_text(encoding="utf-8") == "original\n"


def test_apply_json_spec_replaces_file_after_python_validation(tmp_path: Path) -> None:
    target = tmp_path / "generated.py"
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                        "python": {"functions": ["run"]},
                    },
                ],
            },
        ),
        encoding="utf-8",
    )

    assert main(["apply", "--root", str(tmp_path), "--spec", str(spec)]) == 0
    assert target.read_text(encoding="utf-8") == "def run() -> int:\n    return 0\n"


def test_apply_json_spec_dry_run_validates_without_writing(tmp_path: Path) -> None:
    target = tmp_path / "generated.py"
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                        "python": {"functions": ["run"]},
                    },
                ],
            },
        ),
        encoding="utf-8",
    )

    assert main(["apply", "--root", str(tmp_path), "--spec", str(spec), "--dry-run"]) == 0
    assert not target.exists()


def test_apply_json_spec_runs_post_apply_compile_validation(tmp_path: Path) -> None:
    target = tmp_path / "generated.py"
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                        "python": {"functions": ["run"]},
                    },
                ],
            },
        ),
        encoding="utf-8",
    )

    assert (
        main(
            [
                "apply",
                "--root",
                str(tmp_path),
                "--spec",
                str(spec),
                "--python-path",
                "generated.py",
                "--skip-ruff",
                "--skip-pytest",
            ],
        )
        == 0
    )
    assert target.read_text(encoding="utf-8") == "def run() -> int:\n    return 0\n"


def test_apply_json_spec_runs_spec_level_compile_validation(tmp_path: Path) -> None:
    target = tmp_path / "generated.py"
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                        "python": {"functions": ["run"]},
                    },
                ],
                "validation": {
                    "python_paths": ["generated.py"],
                    "ruff": False,
                    "pytest": False,
                },
            },
        ),
        encoding="utf-8",
    )

    assert main(["apply", "--root", str(tmp_path), "--spec", str(spec)]) == 0
    assert target.read_text(encoding="utf-8") == "def run() -> int:\n    return 0\n"


def test_apply_json_spec_reports_post_apply_validation_failure(tmp_path: Path) -> None:
    target = tmp_path / "generated.py"
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "value = 1\n",
                    },
                ],
            },
        ),
        encoding="utf-8",
    )

    assert (
        main(
            [
                "apply",
                "--root",
                str(tmp_path),
                "--spec",
                str(spec),
                "--python-path",
                "../outside.py",
                "--skip-ruff",
                "--skip-pytest",
            ],
        )
        == 1
    )
    assert not target.exists()


def test_apply_json_spec_dry_run_rejects_escaping_validation_targets(tmp_path: Path) -> None:
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                    },
                ],
                "validation": {
                    "python_paths": ["../outside.py"],
                    "ruff": False,
                    "pytest": False,
                },
            },
        ),
        encoding="utf-8",
    )

    assert main(["apply", "--root", str(tmp_path), "--spec", str(spec), "--dry-run"]) == 1


def test_validate_spec_command_validates_without_writing(tmp_path: Path) -> None:
    target = tmp_path / "generated.py"
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                        "python": {"functions": ["run"]},
                    },
                ],
                "validation": {
                    "python_paths": ["generated.py"],
                    "ruff": False,
                    "pytest": False,
                },
            },
        ),
        encoding="utf-8",
    )

    assert main(["validate-spec", "--root", str(tmp_path), "--spec", str(spec)]) == 0
    assert not target.exists()


def test_validate_spec_command_rejects_escaping_validation_targets(tmp_path: Path) -> None:
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "generated.py",
                        "content": "def run() -> int:\n    return 0\n",
                    },
                ],
                "validation": {
                    "test_paths": ["../outside_test.py"],
                    "ruff": False,
                    "pytest": False,
                },
            },
        ),
        encoding="utf-8",
    )

    assert main(["validate-spec", "--root", str(tmp_path), "--spec", str(spec)]) == 1


def test_repository_patch_engine_example_spec_validates() -> None:
    target = ROOT / "work" / "patch_engine_example.py"

    assert (
        main(
            [
                "validate-spec",
                "--root",
                str(ROOT),
                "--spec",
                str(ROOT / "specs" / "patch-engine-example.json"),
            ],
        )
        == 0
    )
    assert not target.exists()


def test_apply_json_spec_rejects_targets_outside_root(tmp_path: Path) -> None:
    spec = tmp_path / "patch.json"
    spec.write_text(
        json.dumps(
            {
                "operations": [
                    {
                        "type": "replace_file",
                        "path": "../outside.py",
                        "content": "def run() -> int:\n    return 0\n",
                    },
                ],
            },
        ),
        encoding="utf-8",
    )

    assert main(["apply", "--root", str(tmp_path), "--spec", str(spec)]) == 1


def test_run_command_captures_command_result(tmp_path: Path) -> None:
    result = run_command(
        name="probe",
        root=tmp_path,
        arguments=("python3", "-c", "print('ok')"),
    )

    assert result.passed
    assert result.stdout == "ok\n"


def test_validation_plan_can_compile_python_without_external_tools(tmp_path: Path) -> None:
    module = tmp_path / "module.py"
    module.write_text("def run() -> int:\n    return 0\n", encoding="utf-8")

    results = run_validation_plan(
        root=tmp_path,
        python_paths=(module,),
        test_paths=(),
        run_ruff=False,
        run_pytest=False,
    )

    assert [result.name for result in results] == ["python-compile"]


def test_check_command_runs_compile_only(tmp_path: Path) -> None:
    module = tmp_path / "module.py"
    module.write_text("def run() -> int:\n    return 0\n", encoding="utf-8")

    assert (
        main(
            [
                "check",
                "--root",
                str(tmp_path),
                "--python-path",
                "module.py",
                "--skip-ruff",
                "--skip-pytest",
            ],
        )
        == 0
    )
