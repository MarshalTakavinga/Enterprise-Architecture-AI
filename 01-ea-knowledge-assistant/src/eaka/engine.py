"""End-to-end pipeline: build the index, then answer questions from it."""
from __future__ import annotations

import time
from dataclasses import replace

from .answer import (EXCEPTION_NOTICE, NOT_FOUND, NOT_FOUND_MESSAGE, check_groundedness, generate,
                     mentions_exception, to_citations)
from .config import Settings, get_settings
from .embeddings import load_embedder, make_embedder
from .ingest import build_chunks, corpus_fingerprint, load_corpus
from .models import Answer
from .querylog import QueryLog
from .retrieval import Retriever
from .store import make_store


def build_index(settings: Settings | None = None) -> dict:
    s = settings or get_settings()
    docs = load_corpus(s.corpus_dir)
    chunks = build_chunks(docs)
    embedder = make_embedder(s.embedder, s.embedding_model)
    texts = [c.embed_text for c in chunks]
    embedder.fit(texts)
    vectors = embedder.embed(texts)
    s.index_dir.mkdir(parents=True, exist_ok=True)
    embedder.save(s.index_dir / ("lsa.pkl" if s.embedder == "lsa" else "embedder.txt"))
    meta = {
        "corpus_fingerprint": corpus_fingerprint(s.corpus_dir),
        "embedder": embedder.name,
        "dim": int(vectors.shape[1]),
        "documents": len(docs),
        "chunks": len(chunks),
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    make_store(s.store, s.index_dir, s.database_url).write(docs, chunks, vectors, meta)
    return meta


class KnowledgeAssistant:
    def __init__(self, settings: Settings | None = None, auto_index: bool = True):
        self.s = settings or get_settings()
        self.store = make_store(self.s.store, self.s.index_dir, self.s.database_url)
        if not self.store.exists() or (auto_index and self._stale()):
            build_index(self.s)
            self.store = make_store(self.s.store, self.s.index_dir, self.s.database_url)
        self.store.load()
        self.meta = self.store.meta()
        self.embedder = load_embedder(self.s.embedder, self.s.embedding_model, self.s.index_dir)
        self.retriever = Retriever(self.store, self.embedder, lexical_weight=self.s.lexical_weight)
        self.log = QueryLog(self.s.log_dir)

    def _stale(self) -> bool:
        """Re-index automatically when any corpus file changed (Phase 4: no index drift)."""
        try:
            return self.store.meta().get("corpus_fingerprint") != corpus_fingerprint(self.s.corpus_dir)
        except Exception:
            return True

    @property
    def documents(self) -> dict[str, dict]:
        return self.store.docs

    def ask(self, question: str, user: str = "anonymous", provider: str | None = None, log: bool = True) -> Answer:
        t0 = time.perf_counter()
        provider = provider or self.s.llm_provider
        question = question.strip()[:2000]
        results = self.retriever.search(question, k=self.s.top_k)
        ans = Answer(question=question, answer="", found=False, provider=provider,
                     retrieved=[r.chunk.chunk_id for r in results])

        relevance = results[0].raw_relevance if results else 0.0
        if relevance < self.s.min_relevance:
            ans.answer = NOT_FOUND_MESSAGE          # gate: don't even ask the LLM
        else:
            text = generate(provider, question, results, self.s.llm_model, self.s.max_answer_tokens).strip()
            if text == NOT_FOUND or text.startswith(NOT_FOUND):
                ans.answer = NOT_FOUND_MESSAGE
            else:
                ans.found = True
                ans.answer = text
                ans.citations = to_citations(text, results, provider)
                for c in ans.citations:
                    c.source_path = self.documents.get(c.doc_id, {}).get("source_path", "")
                ans.grounded, _ = check_groundedness(text, results)
                if not ans.citations:
                    # An answer with no citation is not a valid answer (governance rule).
                    ans.found, ans.grounded = False, False
                    ans.answer = NOT_FOUND_MESSAGE
                if ans.found and mentions_exception(question, results):
                    ans.governance_notice = EXCEPTION_NOTICE
        ans.latency_ms = int((time.perf_counter() - t0) * 1000)
        if log:
            ans.query_id = self.log.record(ans, user=user, index_version=self.meta.get("corpus_fingerprint", ""))
        return ans

    def with_settings(self, **overrides) -> "KnowledgeAssistant":
        return KnowledgeAssistant(replace(self.s, **overrides))
