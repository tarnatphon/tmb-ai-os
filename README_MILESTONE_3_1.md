# TMB AI OS — Milestone 3.1: AI Agent Framework

This milestone adds a production-oriented, deterministic multi-agent framework.

## Included agents

- Planner Agent
- Writer Agent
- SEO Reviewer Agent
- Brand Reviewer Agent
- Fact Check Agent
- Image Prompt Agent
- QA Agent

## Architecture

```text
Content Brief
    |
    v
Planner
    |
    v
Writer
    |
    +--> SEO Review
    +--> Brand Review
    +--> Fact Check
    |
    v
Image Prompt
    |
    v
QA Decision
```

Agents are registered through a registry and executed by an orchestrator.
The framework uses the existing `TextGenerator` abstraction, so Gemini can be
replaced later without changing the orchestration layer.

## Install

Copy the overlay into the repository root:

```bash
cp -R /path/to/tmb-ai-os-milestone-3-1/. .
```

Apply the API integration:

```bash
python scripts/apply_milestone_3_1.py
```

Run checks:

```bash
ruff format .
ruff check .
mypy src
pytest
```

## API

- `GET /v3/agents`
- `POST /v3/agents/run`
- `POST /v3/workflows/content`

## Expected result

The full suite should pass without making external Gemini calls.
