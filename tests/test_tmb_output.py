from __future__ import annotations

import io
import json

from tools.tmb.output import JSON_SCHEMA_VERSION, build_envelope, emit_json


def test_build_envelope_uses_current_schema_version() -> None:
    payload = build_envelope(
        command="version",
        status="ok",
        data={"version": "0.1.0"},
    )

    assert payload == {
        "schema_version": JSON_SCHEMA_VERSION,
        "command": "version",
        "status": "ok",
        "data": {"version": "0.1.0"},
    }


def test_build_envelope_copies_data_mapping() -> None:
    data = {"healthy": True}

    payload = build_envelope(
        command="doctor",
        status="ok",
        data=data,
    )

    assert payload["data"] == data
    assert payload["data"] is not data


def test_emit_json_produces_valid_json() -> None:
    stream = io.StringIO()

    emit_json(
        {
            "schema_version": 1,
            "command": "version",
            "status": "ok",
            "data": {"synchronized": False},
        },
        stream=stream,
    )

    parsed = json.loads(stream.getvalue())

    assert parsed["schema_version"] == 1
    assert parsed["command"] == "version"
    assert parsed["data"]["synchronized"] is False


def test_emit_json_ends_with_single_newline() -> None:
    stream = io.StringIO()

    emit_json({"status": "ok"}, stream=stream)

    assert stream.getvalue().endswith("\n")
    assert not stream.getvalue().endswith("\n\n")


def test_emit_json_sorts_keys_deterministically() -> None:
    stream = io.StringIO()

    emit_json({"z": 1, "a": 2}, stream=stream)

    output = stream.getvalue()

    assert output.index('"a"') < output.index('"z"')
