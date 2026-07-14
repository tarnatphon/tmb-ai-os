from pathlib import Path

from tmb_ai_os.content import ContentRepository
from tmb_ai_os.service import ContentGenerationService


class FakeGenerator:
    def generate(self, prompt: str) -> str:
        assert "SOURCE CONTENT" in prompt
        return "Generated content"


def test_generation_service_saves_output(tmp_path: Path) -> None:
    content_dir = tmp_path / "content"
    output_dir = tmp_path / "output"
    content_dir.mkdir()
    source = content_dir / "brief.md"
    source.write_text(
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

    service = ContentGenerationService(
        repository=ContentRepository(content_dir),
        generator=FakeGenerator(),
        output_dir=output_dir,
        model_name="fake",
    )

    result = service.generate_from_file(source)

    assert result.text == "Generated content"
    saved = list(output_dir.glob("brief-*.md"))
    assert len(saved) == 1
