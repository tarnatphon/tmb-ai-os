from datetime import UTC, datetime
from pathlib import Path

from .content import ContentRepository
from .domain import GeneratedContent
from .prompts import build_prompt
from .providers import TextGenerator


class ContentGenerationService:
    def __init__(
        self,
        repository: ContentRepository,
        generator: TextGenerator,
        output_dir: Path,
        model_name: str,
    ) -> None:
        self.repository = repository
        self.generator = generator
        self.output_dir = output_dir
        self.model_name = model_name

    def generate_from_file(self, path: Path) -> GeneratedContent:
        brief = self.repository.load_brief(path)
        text = self.generator.generate(build_prompt(brief))
        result = GeneratedContent(
            source_path=brief.source_path,
            model=self.model_name,
            text=text,
        )
        self._save(brief.source_path.stem, result.text)
        return result

    def _save(self, slug: str, text: str) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        output_path = self.output_dir / f"{slug}-{timestamp}.md"
        output_path.write_text(text + "\n", encoding="utf-8")
        return output_path
