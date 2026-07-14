from pathlib import Path
from typing import Any

import frontmatter

from .domain import ContentBrief


class ContentRepository:
    def __init__(self, root: Path) -> None:
        self.root = root

    def list_markdown(self) -> list[Path]:
        if not self.root.exists():
            return []
        return sorted(self.root.rglob("*.md"))

    def load_brief(self, path: Path) -> ContentBrief:
        resolved = path if path.is_absolute() else Path.cwd() / path
        post = frontmatter.load(resolved)
        metadata: dict[str, Any] = dict(post.metadata)

        return ContentBrief(
            source_path=resolved,
            title=str(metadata.pop("title", resolved.stem)),
            topic=str(metadata.pop("topic", resolved.stem)),
            pillar=str(metadata.pop("pillar", "General")),
            audience=self._to_list(metadata.pop("audience", [])),
            channels=self._to_list(metadata.pop("channels", [])),
            language=str(metadata.pop("language", "th")),
            objective=str(metadata.pop("objective", "educate")),
            call_to_action=str(metadata.pop("call_to_action", "")),
            body=post.content.strip(),
            metadata=metadata,
        )

    @staticmethod
    def _to_list(value: Any) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        return []
