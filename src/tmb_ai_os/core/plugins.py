from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True, slots=True)
class PluginManifest:
    name: str
    version: str
    enabled: bool
    capabilities: tuple[str, ...]
    events: tuple[str, ...]
    permissions: tuple[str, ...]
    source: Path


class PluginRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, PluginManifest] = {}

    def discover(self, plugins_dir: Path) -> tuple[PluginManifest, ...]:
        if not plugins_dir.exists():
            return ()
        discovered: list[PluginManifest] = []
        for manifest_path in sorted(plugins_dir.glob("*/plugin.yaml")):
            manifest = self._load_manifest(manifest_path)
            if manifest.name in self._plugins:
                raise ValueError(f"Duplicate plugin name: {manifest.name}")
            self._plugins[manifest.name] = manifest
            discovered.append(manifest)
        return tuple(discovered)

    def list_plugins(self) -> tuple[PluginManifest, ...]:
        return tuple(self._plugins.values())

    @staticmethod
    def _load_manifest(path: Path) -> PluginManifest:
        raw: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"Invalid plugin manifest: {path}")
        for key in ("name", "version"):
            if not isinstance(raw.get(key), str) or not raw[key].strip():
                raise ValueError(f"Missing required field '{key}' in {path}")
        return PluginManifest(
            name=raw["name"],
            version=raw["version"],
            enabled=bool(raw.get("enabled", True)),
            capabilities=tuple(raw.get("capabilities", [])),
            events=tuple(raw.get("events", [])),
            permissions=tuple(raw.get("permissions", [])),
            source=path,
        )
