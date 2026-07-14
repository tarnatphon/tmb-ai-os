# TMB AI OS — Milestone 1

Content-first foundation for Thai Modern Bags.

## What this milestone includes

- Markdown + YAML front matter as the content source of truth
- Gemini provider using the official `google-genai` SDK
- FastAPI endpoints
- CLI commands
- Validation before generation
- Deterministic prompt assembly
- Unit tests that do not call Gemini
- GitHub Actions CI

## Install on macOS

```bash
cd tmb-ai-os
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
cp .env.example .env
```

Add your Gemini API key to `.env`:

```env
TMB_GEMINI_API_KEY=your_key_here
```

## Validate content

```bash
tmb-ai validate
```

## Preview the assembled prompt

```bash
tmb-ai preview content/briefs/oem-bag-100-pcs.md
```

## Generate content

```bash
tmb-ai generate content/briefs/oem-bag-100-pcs.md
```

Generated files are written to `output/`.

## Run API

```bash
uvicorn tmb_ai_os.api:app --reload
```

Then open:

- `GET /health`
- `GET /v1/content`
- `POST /v1/generate`

## Development checks

```bash
ruff check .
mypy src
pytest
```

## Architecture principle

Business content lives in Markdown. Python loads, validates, assembles, and generates.
The AI provider is an adapter and can be replaced without rewriting business content.
