from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app


def test_health_reports_content_first():
    with TestClient(app) as client:
        response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["architecture"] == "content-first"


def test_generate_returns_markdown(monkeypatch):
    from app.content import engine
    from app.providers.base import GenerationResult

    class FakeProvider:
        def generate(self, *, system_prompt: str, user_prompt: str):
            assert "ไม่ใช่ JSON" in system_prompt
            assert "Markdown" in user_prompt
            return GenerationResult(
                text="# Facebook\n\nโพสต์พร้อมใช้",
                model="fake-model",
                provider="fake",
            )

    monkeypatch.setattr(engine, "get_provider", lambda: FakeProvider())
    with TestClient(app) as client:
        response = client.post(
            "/api/content/generate",
            json={"topic": "M1 unique content topic", "pillar": "OEM Manufacturing"},
        )
    assert response.status_code == 200
    body = response.json()
    assert body["markdown"].startswith("# Facebook")
    assert body["provider"] == "fake"


def test_plain_markdown_endpoint(monkeypatch):
    from app.content import engine
    from app.providers.base import GenerationResult

    class FakeProvider:
        def generate(self, **kwargs):
            return GenerationResult("# Blog\n\nReady", "fake-model", "fake")

    monkeypatch.setattr(engine, "get_provider", lambda: FakeProvider())
    with TestClient(app) as client:
        response = client.post(
            "/api/content/generate.md",
            json={"topic": "M1 second unique topic", "pillar": "Education"},
        )
    assert response.status_code == 200
    assert response.text.startswith("# Blog")
    assert response.headers["content-type"].startswith("text/plain")


def test_gemini_provider_uses_plain_text(monkeypatch):
    from app.providers import gemini

    captured = {}

    class FakeModels:
        def list(self):
            return [
                SimpleNamespace(
                    name="models/gemini-current-flash", supported_actions=["generateContent"]
                )
            ]

        def generate_content(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(text="# Content\nReady")

    class FakeClient:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setattr(gemini.genai, "Client", FakeClient)
    monkeypatch.setattr(gemini.settings, "gemini_api_key", "test")
    monkeypatch.setattr(gemini.settings, "ai_model", "auto")
    provider = gemini.GeminiProvider()
    result = provider.generate(system_prompt="system", user_prompt="user")
    assert result.text.startswith("# Content")
    assert captured["config"].response_mime_type == "text/plain"
    assert (
        not hasattr(captured["config"], "response_schema")
        or captured["config"].response_schema is None
    )
