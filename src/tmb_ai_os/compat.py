from importlib import import_module
from types import ModuleType


class LegacyImportError(ImportError):
    pass


def import_legacy_module(name: str) -> ModuleType:
    try:
        return import_module(f"app.{name}")
    except ImportError as exc:
        raise LegacyImportError(f"Legacy module app.{name} could not be imported") from exc
