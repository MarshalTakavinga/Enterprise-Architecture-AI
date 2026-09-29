"""Runtime configuration, read from environment variables (12-factor style).

Every setting has a safe offline default so the project runs end-to-end with no
API keys and no database: lexical + LSA retrieval, in-memory index, extractive answers.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

_SRC_ROOT = Path(__file__).resolve().parents[2]
# Source checkout -> repo root; installed package (e.g. in the container) -> current directory.
PROJECT_ROOT = _SRC_ROOT if (_SRC_ROOT / "data" / "corpus").exists() else Path.cwd()


def _env(name: str, default: str) -> str:
    return os.environ.get(name, default)


@dataclass(frozen=True)
class Settings:
    corpus_dir: Path = field(default_factory=lambda: Path(_env("EAKA_CORPUS_DIR", str(PROJECT_ROOT / "data" / "corpus"))))
    index_dir: Path = field(default_factory=lambda: Path(_env("EAKA_INDEX_DIR", str(PROJECT_ROOT / ".index"))))
    log_dir: Path = field(default_factory=lambda: Path(_env("EAKA_LOG_DIR", str(PROJECT_ROOT / "logs"))))

    # Retrieval
    embedder: str = field(default_factory=lambda: _env("EAKA_EMBEDDER", "lsa"))          # lsa | openai | azure_openai | sentence_transformers
    embedding_model: str = field(default_factory=lambda: _env("EAKA_EMBEDDING_MODEL", "text-embedding-3-small"))
    store: str = field(default_factory=lambda: _env("EAKA_STORE", "memory"))              # memory | pgvector
    database_url: str = field(default_factory=lambda: _env("EAKA_DATABASE_URL", "postgresql://eaka:eaka@localhost:5432/eaka"))
    # Weight of the BM25 ranking relative to the dense ranking in rank fusion (tuned on the dev split).
    lexical_weight: float = field(default_factory=lambda: float(_env("EAKA_LEXICAL_WEIGHT", "0.5")))
    top_k: int = field(default_factory=lambda: int(_env("EAKA_TOP_K", "6")))
    # Answerability gate: below this relevance the assistant says "not found" without calling an LLM.
    # Default = threshold tuned on the eval dev split for the offline (lsa) index; re-tune per embedder.
    min_relevance: float = field(default_factory=lambda: float(_env("EAKA_MIN_RELEVANCE", "0.51")))

    # Generation
    llm_provider: str = field(default_factory=lambda: _env("EAKA_LLM_PROVIDER", "extractive"))  # extractive | anthropic | azure_openai | openai
    llm_model: str = field(default_factory=lambda: _env("EAKA_LLM_MODEL", ""))
    max_answer_tokens: int = field(default_factory=lambda: int(_env("EAKA_MAX_ANSWER_TOKENS", "700")))

    # API protection
    api_keys: tuple[str, ...] = field(default_factory=lambda: tuple(k for k in _env("EAKA_API_KEYS", "").split(",") if k))
    rate_limit_per_minute: int = field(default_factory=lambda: int(_env("EAKA_RATE_LIMIT_PER_MINUTE", "30")))


def get_settings() -> Settings:
    return Settings()
