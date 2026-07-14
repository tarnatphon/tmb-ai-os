import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter


@dataclass(frozen=True)
class KnowledgeDocument:
    path: Path
    title: str
    category: str
    tags: tuple[str, ...]
    body: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class SearchResult:
    document: KnowledgeDocument
    score: float


class KnowledgeRepository:
    def __init__(self, root: Path) -> None:
        self.root = root

    def list_documents(self) -> list[KnowledgeDocument]:
        if not self.root.exists():
            return []
        return [self.load(path) for path in sorted(self.root.rglob("*.md"))]

    def load(self, path: Path) -> KnowledgeDocument:
        resolved = path if path.is_absolute() else Path.cwd() / path
        post = frontmatter.load(resolved)
        metadata: dict[str, Any] = dict(post.metadata)
        tags_value = metadata.pop("tags", [])
        tags = self._to_tuple(tags_value)

        return KnowledgeDocument(
            path=resolved,
            title=str(metadata.pop("title", resolved.stem)),
            category=str(metadata.pop("category", "general")),
            tags=tags,
            body=post.content.strip(),
            metadata=metadata,
        )

    @staticmethod
    def _to_tuple(value: Any) -> tuple[str, ...]:
        if isinstance(value, list):
            return tuple(str(item).strip() for item in value if str(item).strip())
        if isinstance(value, str):
            return tuple(part.strip() for part in value.split(",") if part.strip())
        return ()


class KeywordKnowledgeRetriever:
    def __init__(self, repository: KnowledgeRepository) -> None:
        self.repository = repository

    def search(self, query: str, limit: int = 4) -> list[SearchResult]:
        query_tokens = self._tokens(query)
        if not query_tokens:
            return []

        results: list[SearchResult] = []
        for document in self.repository.list_documents():
            title_tokens = self._tokens(document.title)
            tag_tokens = self._tokens(" ".join(document.tags))
            body_tokens = self._tokens(document.body)

            title_hits = len(query_tokens & title_tokens)
            tag_hits = len(query_tokens & tag_tokens)
            body_hits = len(query_tokens & body_tokens)
            score = title_hits * 4.0 + tag_hits * 2.0 + body_hits * 1.0

            if score > 0:
                results.append(SearchResult(document=document, score=score))

        return sorted(
            results,
            key=lambda result: (-result.score, result.document.title),
        )[: max(1, min(limit, 20))]

    @staticmethod
    def _tokens(text: str) -> set[str]:
        return {
            token.lower() for token in re.findall(r"[\w\u0E00-\u0E7F]+", text) if len(token) > 1
        }
