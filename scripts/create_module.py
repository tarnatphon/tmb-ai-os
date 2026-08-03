from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MODULE_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = ROOT / "templates"


class ModuleGenerationError(RuntimeError):
    """Raised when module generation cannot be completed safely."""


def render(template_name: str, values: dict[str, str]) -> str:
    """Render a repository template using simple named placeholders."""

    template_path = TEMPLATE_DIR / template_name
    if not template_path.is_file():
        raise ModuleGenerationError(f"Template does not exist: {template_path}")

    rendered = template_path.read_text(encoding="utf-8")
    for key, value in values.items():
        rendered = rendered.replace("{{ " + key + " }}", value)

    unresolved = re.findall(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}", rendered)
    if unresolved:
        names = ", ".join(sorted(set(unresolved)))
        raise ModuleGenerationError(f"Unresolved template variables: {names}")

    return rendered


def generate_module(module_name: str) -> tuple[Path, Path]:
    """Generate a source module and matching test without overwriting files."""

    if not MODULE_PATTERN.fullmatch(module_name):
        raise ModuleGenerationError("Module name must use snake_case.")

    class_name = "".join(part.capitalize() for part in module_name.split("_"))
    values = {
        "module_name": module_name,
        "class_name": class_name,
        "package_name": f"tmb_ai_os.{module_name}",
    }

    source_path = ROOT / "src" / "tmb_ai_os" / f"{module_name}.py"
    test_path = ROOT / "tests" / f"test_{module_name}.py"

    existing_paths = [path for path in (source_path, test_path) if path.exists()]
    if existing_paths:
        paths = ", ".join(str(path) for path in existing_paths)
        raise ModuleGenerationError(f"Refusing to overwrite existing files: {paths}")

    source_content = render("python_module.py.j2", values)
    test_content = render("pytest_module.py.j2", values)

    source_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.parent.mkdir(parents=True, exist_ok=True)

    source_path.write_text(source_content, encoding="utf-8")
    try:
        test_path.write_text(test_content, encoding="utf-8")
    except OSError:
        source_path.unlink(missing_ok=True)
        raise

    return source_path, test_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new TMB AI OS module from repository templates."
    )
    parser.add_argument("module_name", help="Module name in snake_case")
    args = parser.parse_args()

    try:
        source_path, test_path = generate_module(args.module_name)
    except (ModuleGenerationError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Created {source_path}")
    print(f"Created {test_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
