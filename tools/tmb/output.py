from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from typing import Any, TextIO

JSON_SCHEMA_VERSION = 1


def build_envelope(
    *,
    command: str,
    status: str,
    data: Mapping[str, Any],
) -> dict[str, Any]:
    """Build the stable machine-readable CLI response envelope."""

    return {
        "schema_version": JSON_SCHEMA_VERSION,
        "command": command,
        "status": status,
        "data": dict(data),
    }


def emit_json(
    payload: Mapping[str, Any],
    *,
    stream: TextIO | None = None,
) -> None:
    """Write JSON output without additional human-readable text."""

    destination = stream if stream is not None else sys.stdout
    json.dump(
        payload,
        destination,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    destination.write("\n")
