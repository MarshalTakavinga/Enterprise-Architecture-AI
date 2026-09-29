"""Hybrid retrieval: BM25 + dense vectors fused with Reciprocal Rank Fusion (RRF),
an exact-identifier boost, per-document diversity, and a relevance gate that decides
whether the corpus can answer the question at all.
"""
from __future__ import annotations

import re

from .embeddings import Embedder
from .lexical import BM25
from .models import ScoredChunk

DOC_ID = re.compile(r"\b(STD-[A-Z]{2,3}-\d{3}|ADR-\d{4}|AP-\d{2}|RA-0\d|GOV-0\d|PRE-0\d|A-0\d|ADD-0\d|ARS-0\d|F-0\d|G-0\d|H-0\d)\b", re.I)
RRF_K = 60
CANDIDATES = 40
MAX_PER_DOC = 3


class Retriever:
    def __init__(self, store, embedder: Embedder, lexical_weight: float = 1.0, dense_weight: float = 1.0):
        self.store = store
        self.embedder = embedder
        self.chunks = store.load_chunks()
        self.bm25 = BM25().fit([c.embed_text for c in self.chunks])
        self.lw, self.dw = lexical_weight, dense_weight

    def search(self, query: str, k: int = 6) -> list[ScoredChunk]:
        n = len(self.chunks)
        lex = self.bm25.scores(query)
        lex_rank = sorted(range(n), key=lambda i: -lex[i])[:CANDIDATES]
        qvec = self.embedder.embed([query])[0]
        dense = self.store.dense_search(qvec, CANDIDATES)
        dense_sim = {i: s for i, s in dense}

        fused: dict[int, float] = {}
        for r, i in enumerate(lex_rank):
            if lex[i] > 0:
                fused[i] = fused.get(i, 0.0) + self.lw / (RRF_K + r + 1)
        for r, (i, _) in enumerate(dense):
            fused[i] = fused.get(i, 0.0) + self.dw / (RRF_K + r + 1)

        mentioned = {m.upper() for m in DOC_ID.findall(query)}
        if mentioned:
            for i, c in enumerate(self.chunks):
                if c.doc_id.upper() in mentioned:
                    fused[i] = fused.get(i, 0.0) + 1.0 / RRF_K  # strong but not absolute boost

        ranked = sorted(fused, key=lambda i: -fused[i])
        per_doc: dict[str, int] = {}
        out: list[ScoredChunk] = []
        top = fused[ranked[0]] if ranked else 1.0
        max_lex = max(lex) if lex else 0.0
        for i in ranked:
            c = self.chunks[i]
            if per_doc.get(c.doc_id, 0) >= MAX_PER_DOC:
                continue
            per_doc[c.doc_id] = per_doc.get(c.doc_id, 0) + 1
            out.append(ScoredChunk(
                chunk=c,
                score=fused[i] / top,
                lexical_score=lex[i] / max_lex if max_lex else 0.0,
                dense_score=dense_sim.get(i, 0.0),
            ))
            if len(out) == k:
                break
        rel = self.relevance(query, out)
        for s in out:
            s.raw_relevance = rel
        return out

    def relevance(self, query: str, results: list[ScoredChunk]) -> float:
        """Absolute answerability signal in [0, 1].

        Ranks alone can't say "nothing here is relevant"; this can. It combines
          (a) corpus coverage — share of the query's informative (idf-weighted) terms that exist
              anywhere in the corpus ('COBOL', 'blockchain' don't);
          (b) passage coverage — the best share of those terms found together in ONE of the top
              passages (an out-of-corpus question's words are scattered: 'travel' here, 'expense'
              there — a real answer's are co-located);
          (c) the best dense similarity.
        The threshold is tuned on the eval dev split only (see eval/README.md).
        """
        if not results:
            return 0.0
        coverage = self.bm25.query_coverage(query)
        passage = max(self.bm25.passage_coverage(query, r.chunk.embed_text) for r in results[:3])
        best_dense = max((r.dense_score for r in results), default=0.0)
        return 0.4 * coverage + 0.4 * passage + 0.2 * max(best_dense, 0.0)
