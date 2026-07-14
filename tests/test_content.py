from pathlib import Path

from tmb_ai_os.content import ContentRepository


def test_load_brief(tmp_path: Path) -> None:
    path = tmp_path / "brief.md"
    path.write_text(
        """---
title: Test Brief
topic: OEM Bags
pillar: Manufacturing
audience: [Business owners]
channels: [website]
objective: educate
---
This is sufficiently long source content.
""",
        encoding="utf-8",
    )

    brief = ContentRepository(tmp_path).load_brief(path)

    assert brief.title == "Test Brief"
    assert brief.audience == ["Business owners"]
    assert brief.body.startswith("This is")
