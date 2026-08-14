from __future__ import annotations

import argparse
import json
from collections.abc import Sequence
from pathlib import Path

from . import PatchEngineError, PatchValidationError
from .models import (
    ReplaceFileOperation,
    ValidationPlan,
    parse_replace_file_operation,
    parse_validation_plan,
)
from .parser import parse_python_file, parse_python_source
from .runner import CommandResult, run_validation_plan
from .transaction import PatchTransaction
from .validator import PythonStructureRequirement, validate_python_structure


def build_parser() -> argparse.ArgumentParser:
    """Build the patch engine CLI parser."""

    parser = argparse.ArgumentParser(
        prog="patch-engine",
        description="Apply validated repository patch operations.",
    )
    subparsers = parser.add_subparsers(dest="command")

    validate_parser = subparsers.add_parser(
        "validate-python",
        help="Validate Python syntax and expected top-level structure.",
    )
    validate_parser.add_argument("path")
    validate_parser.add_argument("--require-function", action="append", default=[])
    validate_parser.add_argument("--require-class", action="append", default=[])
    validate_parser.set_defaults(handler=run_validate_python)

    apply_parser = subparsers.add_parser(
        "apply",
        help="Apply a JSON patch spec transactionally.",
    )
    apply_parser.add_argument("--spec", required=True)
    apply_parser.add_argument("--root", default=".")
    apply_parser.add_argument("--dry-run", action="store_true")
    apply_parser.add_argument("--python-path", action="append", default=[])
    apply_parser.add_argument("--test-path", action="append", default=[])
    apply_parser.add_argument("--skip-ruff", action="store_true")
    apply_parser.add_argument("--skip-pytest", action="store_true")
    apply_parser.set_defaults(handler=run_apply)

    spec_parser = subparsers.add_parser(
        "validate-spec",
        help="Validate a JSON patch spec without writing files.",
    )
    spec_parser.add_argument("--spec", required=True)
    spec_parser.add_argument("--root", default=".")
    spec_parser.set_defaults(handler=run_validate_spec)

    check_parser = subparsers.add_parser(
        "check",
        help="Run patch validation checks.",
    )
    check_parser.add_argument("--root", default=".")
    check_parser.add_argument("--python-path", action="append", default=[])
    check_parser.add_argument("--test-path", action="append", default=[])
    check_parser.add_argument("--skip-ruff", action="store_true")
    check_parser.add_argument("--skip-pytest", action="store_true")
    check_parser.set_defaults(handler=run_check)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the patch engine CLI."""

    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)

    if handler is None:
        parser.print_help()
        return 0

    try:
        return int(handler(args))
    except PatchEngineError as exc:
        print(f"Patch engine failed: {exc}")
        return 1


def run_validate_python(args: argparse.Namespace) -> int:
    """Validate a Python file from CLI arguments."""

    module = parse_python_file(Path(args.path))
    validate_python_structure(
        module,
        PythonStructureRequirement(
            functions=tuple(args.require_function),
            classes=tuple(args.require_class),
        ),
    )
    print("Python validation PASSED")
    return 0


def run_apply(args: argparse.Namespace) -> int:
    """Apply a JSON patch spec."""

    root = Path(args.root).resolve()
    operations, validation_plan = _load_spec(Path(args.spec), root=root)

    for operation in operations:
        if operation.python is not None:
            module = parse_python_source(operation.content, path=operation.path)
            validate_python_structure(module, operation.python)

    if args.dry_run:
        _validate_validation_targets(root=root, validation_plan=validation_plan)
        print(f"Validated {len(operations)} operation(s)")
        return 0

    transaction = PatchTransaction()
    transaction.apply(
        tuple(operation.to_replacement() for operation in operations),
        commit=False,
    )

    try:
        validation_results = _run_post_apply_validation(
            args,
            root=root,
            validation_plan=validation_plan,
        )
    except PatchValidationError:
        transaction.rollback()
        raise

    transaction.commit()
    for result in validation_results:
        print(_format_result(result))

    print(f"Applied {len(operations)} operation(s)")
    return 0


def run_validate_spec(args: argparse.Namespace) -> int:
    """Validate a JSON patch spec without applying it."""

    root = Path(args.root).resolve()
    operations, validation_plan = _load_spec(Path(args.spec), root=root)

    for operation in operations:
        if operation.python is not None:
            module = parse_python_source(operation.content, path=operation.path)
            validate_python_structure(module, operation.python)

    _validate_validation_targets(root=root, validation_plan=validation_plan)
    print(f"Spec validation PASSED ({len(operations)} operation(s))")
    return 0


def run_check(args: argparse.Namespace) -> int:
    """Run patch validation checks from CLI arguments."""

    results = run_validation_plan(
        root=Path(args.root).resolve(),
        python_paths=tuple(Path(path) for path in args.python_path),
        test_paths=tuple(Path(path) for path in args.test_path),
        run_ruff=not args.skip_ruff,
        run_pytest=not args.skip_pytest,
    )

    for result in results:
        print(_format_result(result))

    return 0


def _format_result(result: CommandResult) -> str:
    status = "PASS" if result.passed else "FAIL"
    return f"[{status}] {result.name}"


def _run_post_apply_validation(
    args: argparse.Namespace,
    *,
    root: Path,
    validation_plan: ValidationPlan,
) -> tuple[CommandResult, ...]:
    python_paths = validation_plan.python_paths + tuple(Path(path) for path in args.python_path)
    test_paths = validation_plan.test_paths + tuple(Path(path) for path in args.test_path)

    if not python_paths and not test_paths:
        return ()

    return run_validation_plan(
        root=root,
        python_paths=python_paths,
        test_paths=test_paths,
        run_ruff=validation_plan.run_ruff and not args.skip_ruff,
        run_pytest=validation_plan.run_pytest and not args.skip_pytest and bool(test_paths),
    )


def _validate_validation_targets(*, root: Path, validation_plan: ValidationPlan) -> None:
    for path in validation_plan.python_paths + validation_plan.test_paths:
        resolved_path = (root / path).resolve() if not path.is_absolute() else path.resolve()
        try:
            resolved_path.relative_to(root.resolve())
        except ValueError as exc:
            message = f"validation target escapes repository root: {path}"
            raise PatchValidationError(message) from exc


def _load_spec(
    spec_path: Path,
    *,
    root: Path,
) -> tuple[tuple[ReplaceFileOperation, ...], ValidationPlan]:
    try:
        raw = json.loads(spec_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PatchValidationError(f"{spec_path}: invalid JSON patch spec") from exc

    if not isinstance(raw, dict):
        raise PatchValidationError("patch spec must be a JSON object")

    operations = raw.get("operations")
    if not isinstance(operations, list):
        raise PatchValidationError("patch spec requires an operations list")

    parsed: list[ReplaceFileOperation] = []
    for operation in operations:
        if not isinstance(operation, dict):
            raise PatchValidationError("each operation must be an object")
        parsed.append(parse_replace_file_operation(operation, root=root))

    _validate_unique_operation_targets(tuple(parsed))
    return tuple(parsed), parse_validation_plan(raw.get("validation"))


def _validate_unique_operation_targets(operations: tuple[ReplaceFileOperation, ...]) -> None:
    seen: set[Path] = set()

    for operation in operations:
        if operation.path in seen:
            raise PatchValidationError(f"duplicate patch target: {operation.path}")
        seen.add(operation.path)
