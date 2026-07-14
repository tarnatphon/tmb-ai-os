from pathlib import Path

from tmb_ai_os.domain import ContentBrief
from tmb_ai_os.prompts import build_prompt


def test_build_prompt_contains_source_and_constraints() -> None:
    brief = ContentBrief(
        source_path=Path("brief.md"),
        title="OEM Bags",
        topic="OEM Bags",
        pillar="Manufacturing",
        audience=["Purchasing"],
        channels=["website"],
        language="th",
        objective="educate",
        body="Verified factory information.",
    )

    prompt = build_prompt(brief)

    assert "Verified factory information." in prompt
    assert "Do not invent" in prompt
    assert "Purchasing" in prompt
