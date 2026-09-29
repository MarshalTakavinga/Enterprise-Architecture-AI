import os
import sys
from dataclasses import replace
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


@pytest.fixture(scope="session")
def settings(tmp_path_factory):
    from eaka.config import get_settings

    tmp = tmp_path_factory.mktemp("eaka")
    return replace(get_settings(), index_dir=tmp / "index", log_dir=tmp / "logs",
                   store="memory", embedder="lsa", llm_provider="extractive")


@pytest.fixture(scope="session")
def ka(settings):
    from eaka.engine import KnowledgeAssistant

    return KnowledgeAssistant(settings)


@pytest.fixture
def api_client(settings, monkeypatch):
    from fastapi.testclient import TestClient

    monkeypatch.setenv("EAKA_INDEX_DIR", str(settings.index_dir))
    monkeypatch.setenv("EAKA_LOG_DIR", str(settings.log_dir))
    monkeypatch.setenv("EAKA_API_KEYS", "test-key")
    from eaka import api

    api.assistant.cache_clear()
    api._hits.clear()
    return TestClient(api.app)
