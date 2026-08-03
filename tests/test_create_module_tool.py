from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest


def load_tool(script_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location("create_module_tool", script_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load create_module.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_tooling(tmp_path: Path) -> ModuleType:
    repository_root = tmp_path / "repository"
    script_dir = repository_root / "scripts"
    template_dir = repository_root / "templates"

    script_dir.mkdir(parents=True)
    template_dir.mkdir(parents=True)

    source_root = Path(__file__).resolve().parents[1]
    script_path = script_dir / "create_module.py"
    script_path.write_text(
        (source_root / "scripts" / "create_module.py").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (template_dir / "python_module.py.j2").write_text(
        (source_root / "templates" / "python_module.py.j2").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (template_dir / "pytest_module.py.j2").write_text(
        (source_root / "templates" / "pytest_module.py.j2").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    return load_tool(script_path)


def test_generate_module_creates_source_and_test(tmp_path: Path) -> None:
    tool = prepare_tooling(tmp_path)

    source_path, test_path = tool.generate_module("sample_module")

    assert source_path.is_file()
    assert test_path.is_file()
    assert "class SampleModule:" in source_path.read_text(encoding="utf-8")
    assert "from tmb_ai_os.sample_module import SampleModule" in test_path.read_text(
        encoding="utf-8"
    )


def test_generate_module_rejects_invalid_name(tmp_path: Path) -> None:
    tool = prepare_tooling(tmp_path)

    with pytest.raises(tool.ModuleGenerationError, match="snake_case"):
        tool.generate_module("Invalid-Name")


def test_generate_module_refuses_to_overwrite(tmp_path: Path) -> None:
    tool = prepare_tooling(tmp_path)
    tool.generate_module("sample_module")

    with pytest.raises(tool.ModuleGenerationError, match="Refusing to overwrite"):
        tool.generate_module("sample_module")


def test_render_rejects_missing_template(tmp_path: Path) -> None:
    tool = prepare_tooling(tmp_path)

    with pytest.raises(tool.ModuleGenerationError, match="Template does not exist"):
        tool.render("missing.py.j2", {})


def test_render_rejects_unresolved_variables(tmp_path: Path) -> None:
    tool = prepare_tooling(tmp_path)
    template_path = Path(tool.TEMPLATE_DIR) / "broken.py.j2"
    template_path.write_text("{{ missing_value }}", encoding="utf-8")

    with pytest.raises(tool.ModuleGenerationError, match="Unresolved template variables"):
        tool.render("broken.py.j2", {})
