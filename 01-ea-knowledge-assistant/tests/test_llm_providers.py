"""LLM provider plumbing, tested with fake clients (no network, no keys)."""
from types import SimpleNamespace

import pytest

from eaka import answer
from eaka.models import Chunk, ScoredChunk

SRC = [ScoredChunk(chunk=Chunk("T#1", "T", "Test", "standard", "§1", "Retention is 7 days."), score=1.0)]


class FakeCompletions:
    """Behaves like a GPT-5-family model: rejects temperature and max_tokens."""

    def __init__(self):
        self.calls = []

    def create(self, **kw):
        self.calls.append(sorted(kw))
        if "temperature" in kw:
            raise Exception("Unsupported value: 'temperature' does not support 0 with this model.")
        if "max_tokens" in kw:
            raise Exception("Unsupported parameter: 'max_tokens'")
        msg = SimpleNamespace(content="Retention is 7 days [1].")
        return SimpleNamespace(choices=[SimpleNamespace(message=msg)])


def test_openai_retries_without_unsupported_params(monkeypatch):
    fake = FakeCompletions()
    monkeypatch.setattr(answer, "openai_client", lambda azure: SimpleNamespace(chat=SimpleNamespace(completions=fake)))
    out = answer.generate("openai", "retention?", SRC, model="gpt-5-mini")
    assert out == "Retention is 7 days [1]."
    assert fake.calls[0] == ["max_completion_tokens", "messages", "model", "temperature"]
    assert fake.calls[-1] == ["max_completion_tokens", "messages", "model"]


def test_azure_needs_a_deployment(monkeypatch):
    monkeypatch.delenv("AZURE_OPENAI_DEPLOYMENT", raising=False)
    with pytest.raises(RuntimeError, match="AZURE_OPENAI_DEPLOYMENT"):
        answer.resolve_model("azure_openai", "")


def test_azure_client_uses_v1_endpoint(monkeypatch):
    pytest.importorskip("openai")
    monkeypatch.setenv("AZURE_OPENAI_ENDPOINT", "https://hlg-aoai.openai.azure.com/")
    monkeypatch.setenv("AZURE_OPENAI_API_KEY", "k" * 32)
    monkeypatch.delenv("AZURE_OPENAI_API_VERSION", raising=False)
    c = answer.openai_client(azure=True)
    assert str(c.base_url) == "https://hlg-aoai.openai.azure.com/openai/v1/"


def test_llm_failure_is_reported_not_raised(ka, monkeypatch):
    def boom(*a, **k):
        raise RuntimeError("401 invalid key")
    monkeypatch.setattr("eaka.engine.generate", boom)
    a = ka.ask("Where must personal data about EU customers be stored?", provider="openai", log=False)
    assert not a.found and "401 invalid key" in a.error and "eaka check" in a.answer
