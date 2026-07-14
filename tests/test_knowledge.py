from pathlib import Path

from tmb_ai_os.knowledge import (
    KeywordKnowledgeRetriever,
    KnowledgeRepository,
)


def test_search_prioritizes_title_and_tags(tmp_path: Path) -> None:
    path = tmp_path / "moq.md"
    path.write_text(
        """---
title: จำนวนขั้นต่ำการผลิต
category: manufacturing
tags: [MOQ, 100 ใบ]
---
จำนวนจริงขึ้นอยู่กับรูปแบบและวัตถุดิบ
""",
        encoding="utf-8",
    )

    retriever = KeywordKnowledgeRetriever(KnowledgeRepository(tmp_path))
    results = retriever.search("MOQ 100 ใบ")

    assert len(results) == 1
    assert results[0].document.title == "จำนวนขั้นต่ำการผลิต"
    assert results[0].score > 0
