# Patch Engine

The patch engine applies repository changes from JSON specs with validation and transactional rollback.

## Commands

Validate a spec without writing files:

```bash
python -m tools.patch_engine validate-spec --spec specs/patch-engine-example.json
```

Validate a spec and preview whether it is structurally safe:

```bash
python -m tools.patch_engine apply --spec specs/patch-engine-example.json --dry-run
```

Apply a spec and run the validation plan declared by the spec:

```bash
python -m tools.patch_engine apply --spec specs/patch-engine-example.json
```

Run ad hoc validation checks:

```bash
python -m tools.patch_engine check \
  --python-path tools/tmb/commands/validate.py \
  --test-path tests/test_tmb_cli_json_output.py
```

## Spec Format

```json
{
  "operations": [
    {
      "type": "replace_file",
      "path": "tools/example.py",
      "content": "def run() -> int:\n    return 0\n",
      "python": {
        "functions": ["run"],
        "classes": []
      }
    }
  ],
  "validation": {
    "python_paths": ["tools/example.py"],
    "test_paths": ["tests/test_example.py"],
    "ruff": true,
    "pytest": true
  }
}
```

## Safety Rules

- Patch targets must stay inside the repository root.
- Patch targets must be unique within one spec.
- Validation targets must stay inside the repository root.
- Python operations can require top-level functions and classes before writing.
- Failed writes roll back previous writes in the same transaction.
- Failed post-apply validation rolls back the transaction.
- `validate-spec` and `apply --dry-run` do not write files.

## Validation Plan

The optional top-level `validation` object lets a spec carry its own checks:

- `python_paths`: files compiled with `py_compile`.
- `test_paths`: tests passed to `pytest`.
- `ruff`: whether to run `ruff check` and `ruff format --check`.
- `pytest`: whether to run pytest for `test_paths`.

CLI validation paths are added to spec validation paths. CLI skip flags can disable Ruff or pytest for a run.
