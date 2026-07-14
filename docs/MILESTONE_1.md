# Milestone 1 — Content-first Foundation

## Delivered

- Provider abstraction (`AIProvider`) and Gemini implementation
- Provider factory selected through `AI_PROVIDER`
- Model discovery, retry, fallback, and normalized provider errors
- Content engine that returns publication-ready Markdown
- External prompt template in `app/prompts/content_package.md`
- JSON structured-output dependency removed from Gemini generation
- Plain Markdown API endpoint
- Copy/download dashboard
- GitHub Actions CI and focused tests

## Compatibility

The existing SQLite `ContentRun.payload_json` column is retained. It now stores a small envelope containing topic, pillar, provider, model, and one Markdown document. This avoids a destructive database migration in Milestone 1.

## Deferred

- Platform-specific agents and parallel generation
- OpenAI/Anthropic/Ollama providers
- Full Markdown renderer package
- DOCX/PDF export
- RAG and knowledge base
