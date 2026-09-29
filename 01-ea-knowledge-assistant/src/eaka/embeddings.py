"""Embedding back-ends behind one small interface.

* ``lsa``  — TF-IDF + truncated SVD (latent semantic analysis). Runs offline with no model
             download; the default so the project works anywhere, and the baseline in /eval.
* ``openai`` / ``azure_openai`` — hosted embedding models (e.g. text-embedding-3-small).
  Azure OpenAI is the choice when data residency matters (see docs/adr/ADR-P003).
* ``sentence_transformers`` — local open model (e.g. BAAI/bge-small-en-v1.5), no data leaves the host.
"""
from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Protocol

import numpy as np


class Embedder(Protocol):
    name: str
    dim: int

    def fit(self, texts: list[str]) -> None: ...
    def embed(self, texts: list[str]) -> np.ndarray: ...
    def save(self, path: Path) -> None: ...


def _normalise(m: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(m, axis=1, keepdims=True)
    n[n == 0] = 1.0
    return (m / n).astype(np.float32)


class LsaEmbedder:
    """Corpus-fitted semantic space; captures co-occurrence (e.g. 'NoSQL' ~ 'Cosmos DB')."""

    name = "lsa"

    def __init__(self, dim: int = 256):
        self.dim = dim
        self._vec = None
        self._svd = None

    def fit(self, texts: list[str]) -> None:
        from sklearn.decomposition import TruncatedSVD
        from sklearn.feature_extraction.text import TfidfVectorizer

        self._vec = TfidfVectorizer(sublinear_tf=True, ngram_range=(1, 2), min_df=1,
                                    stop_words="english", token_pattern=r"(?u)\b[\w][\w\-\.]*\w\b|\b\w\b")
        x = self._vec.fit_transform(texts)
        self.dim = min(self.dim, x.shape[1] - 1, x.shape[0] - 1)
        self._svd = TruncatedSVD(n_components=self.dim, random_state=42)
        self._svd.fit(x)

    def embed(self, texts: list[str]) -> np.ndarray:
        if self._vec is None:
            raise RuntimeError("LsaEmbedder must be fitted (run ingestion) before use")
        return _normalise(self._svd.transform(self._vec.transform(texts)))

    def save(self, path: Path) -> None:
        path.write_bytes(pickle.dumps({"vec": self._vec, "svd": self._svd, "dim": self.dim}))

    @classmethod
    def load(cls, path: Path) -> "LsaEmbedder":
        d = pickle.loads(path.read_bytes())  # local file written by our own ingestion step
        e = cls(d["dim"])
        e._vec, e._svd = d["vec"], d["svd"]
        return e


class OpenAIEmbedder:
    """OpenAI or Azure OpenAI embeddings (set EAKA_EMBEDDER=azure_openai for in-region processing)."""

    def __init__(self, model: str, azure: bool = False):
        from openai import AzureOpenAI, OpenAI

        self.name = ("azure_openai:" if azure else "openai:") + model
        self.model = model
        self.client = (
            AzureOpenAI(api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-10-21"))
            if azure else OpenAI()
        )
        self.dim = 0

    def fit(self, texts: list[str]) -> None:  # hosted models are pre-trained
        pass

    def embed(self, texts: list[str]) -> np.ndarray:
        out = []
        for i in range(0, len(texts), 128):
            resp = self.client.embeddings.create(model=self.model, input=texts[i:i + 128])
            out.extend(d.embedding for d in resp.data)
        m = _normalise(np.array(out, dtype=np.float32))
        self.dim = m.shape[1]
        return m

    def save(self, path: Path) -> None:
        path.write_text(self.name)


class SentenceTransformerEmbedder:
    def __init__(self, model: str):
        from sentence_transformers import SentenceTransformer

        self.name = "sentence_transformers:" + model
        self._m = SentenceTransformer(model)
        self.dim = self._m.get_sentence_embedding_dimension()

    def fit(self, texts: list[str]) -> None:
        pass

    def embed(self, texts: list[str]) -> np.ndarray:
        return _normalise(np.asarray(self._m.encode(texts, batch_size=32), dtype=np.float32))

    def save(self, path: Path) -> None:
        path.write_text(self.name)


def make_embedder(kind: str, model: str) -> Embedder:
    if kind == "lsa":
        return LsaEmbedder()
    if kind in ("openai", "azure_openai"):
        return OpenAIEmbedder(model, azure=kind == "azure_openai")
    if kind == "sentence_transformers":
        return SentenceTransformerEmbedder(model if "/" in model else "BAAI/bge-small-en-v1.5")
    raise ValueError(f"Unknown embedder: {kind}")


def load_embedder(kind: str, model: str, index_dir: Path) -> Embedder:
    if kind == "lsa":
        return LsaEmbedder.load(index_dir / "lsa.pkl")
    return make_embedder(kind, model)
