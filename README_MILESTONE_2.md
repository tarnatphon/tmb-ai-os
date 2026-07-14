# TMB AI OS — Milestone 2

Milestone 2 extends the Content-first foundation with:

- Multi-channel content generation
- Reusable Prompt SDK
- Markdown knowledge base
- Lightweight retrieval suitable for later vector database migration
- Workflow states: draft → generated → reviewed → approved → published
- API endpoints for channel generation and knowledge search
- CLI commands
- Unit tests without external AI calls

## Merge into the existing repository

Back up or commit current work first.

```bash
git status
git add .
git commit -m "chore: checkpoint before milestone 2"
```

Copy this overlay into the repository root:

```bash
cp -R /path/to/tmb-ai-os-milestone-2/. .
```

Install:

```bash
source .venv/bin/activate
pip install -e ".[dev]"
```

Run checks:

```bash
ruff format .
ruff check .
mypy src
pytest
```

## New commands

```bash
tmb-ai knowledge-list
tmb-ai knowledge-search "ขั้นต่ำการผลิต"
tmb-ai multi-preview content/briefs/oem-bag-100-pcs.md
tmb-ai multi-generate content/briefs/oem-bag-100-pcs.md
```

## New API

- `GET /v2/knowledge`
- `GET /v2/knowledge/search?q=...`
- `POST /v2/content/preview`
- `POST /v2/content/generate`

## Content workflow

```text
draft -> generated -> reviewed -> approved -> published
                  \-> rejected -> draft
```

The initial knowledge retriever uses deterministic token matching.
It is intentionally replaceable by pgvector, Chroma, Pinecone, or another
vector store in a later milestone.
