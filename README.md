<<<<<<< HEAD
# tmb-ai-os
แพลตฟอร์ม Enterprise AI สำหรับธุรกิจโรงงาน OEM
=======
# TMB AI OS

Thai Modern Bags Enterprise AI Operating System is a modular platform for building
AI-assisted marketing, sales, production, purchasing, finance, and executive workflows.
Milestone 1 delivers the content-first foundation and a working Gemini-backed marketing service.

## Current capabilities

- Markdown is the canonical AI content output.
- Gemini is isolated behind a provider interface.
- Automatic model discovery, retry, and fallback handle model changes and temporary 503 errors.
- Prompts are versioned under `app/prompts/` instead of embedded in Python.
- FastAPI exposes JSON metadata and plain Markdown endpoints.
- SQLite stores draft history without requiring external infrastructure.
- GitHub Actions validates formatting, lint, compilation, and tests.
- Docker and local macOS workflows are included.

## Architecture

```text
FastAPI API
  -> Content Engine
     -> Prompt Loader
     -> Provider Factory
        -> Gemini Provider
     -> Markdown Renderer
  -> Draft Repository (SQLite)
```

Future modules live behind stable boundaries:

```text
app/
├── agents/        # Marketing, sales, factory and executive agents
├── providers/     # Gemini and future OpenAI/Anthropic/Ollama adapters
├── content/       # Content-first orchestration
├── prompts/       # Versioned prompt SDK
├── renderers/     # Markdown now; HTML/DOCX/PDF later
├── knowledge/     # RAG and governed company knowledge
├── workflows/     # Multi-agent and automation workflows
└── integrations/  # WordPress, LINE OA, n8n, MCP, ERP and CRM
```

## Local setup on macOS

```bash
brew install python@3.13
git clone https://github.com/tarnatphon/tmb-ai-os.git
cd tmb-ai-os
./scripts/bootstrap.sh
nano .env
```

Required environment values:

```env
AI_PROVIDER=gemini
AI_MODEL=auto
GEMINI_API_KEY=your_google_ai_studio_api_key
```

Run the application:

```bash
source .venv/bin/activate
make run
```

Open `http://127.0.0.1:8000`.

## API

- `GET /api/health`
- `POST /api/content/generate` — metadata plus Markdown
- `POST /api/content/generate.md` — plain Markdown response
- `GET /api/content` — draft history

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/content/generate.md \
  -H 'Content-Type: application/json' \
  -d '{"topic":"รับผลิตกระเป๋าขั้นต่ำ 100 ใบ","pillar":"OEM Manufacturing"}'
```

## Quality checks

```bash
make install-dev
make check
```

## Git workflow

Development uses `develop` as the integration branch and focused feature branches:

```bash
git checkout develop
git checkout -b feature/content-agent
git add .
git commit -m "feat(agent): add content planning agent"
git push -u origin feature/content-agent
```

See `CONTRIBUTING.md`, `SECURITY.md`, and `docs/development/BRANCHING.md`.

## Roadmap

- M1: provider layer, prompt SDK, Markdown output, CI and documentation
- M2: platform-specific content agents and validation
- M3: multi-agent planning, writing, SEO and QA workflows
- M4: frontend, preview and export
- M5: knowledge base and RAG
- M6: enterprise operational agents and integrations

This repository is proprietary to Thai Modern Bags Co., Ltd.
>>>>>>> 3e92d53 (feat(core): initialize TMB AI OS foundation)
