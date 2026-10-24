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
# "How long are logs retained and can they contain personal data?" is two questions. Split only
# where "and"/"also" is followed by a new question word, so "API and event standards" stays whole.
COMPOUND = re.compile(r"\s*[,;]?\s+(?:and|also)\s+(?=(?:can|could|is|are|do|does|did|how|what|when|where|which|who|why|should|must|may|will)\b)", re.I)
LEX_HEAD = 1         # BM25's top hit always survives fusion and the per-doc cap (exact-term match, precise)
DENSE_HEAD = 0       # not for the dense head: with the offline LSA embedder it is too noisy (eval q23)
SUB_HEADS = 2        # for compound questions, the top hits of each sub-question also survive
MAX_EXTRA = 2        # guaranteed passages may grow the context from k to at most k + MAX_EXTRA


class Retriever:
    def __init__(self, store, embedder: Embedder, lexical_weight: float = 1.0, dense_weight: float = 1.0):
        self.store = store
        self.embedder = embedder
        self.chunks = store.load_chunks()
        self.bm25 = BM25().fit([c.embed_text for c in self.chunks])
        self.lw, self.dw = lexical_weight, dense_weight

    def search(self, query: str, k: int = 6, max_extra: int = 0) -> list[ScoredChunk]:
        """Top-k passages. With ``max_extra`` > 0 (the answer pipeline uses MAX_EXTRA), guaranteed
        passages that fusion would have dropped are appended, so up to k + max_extra come back."""
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
        # RRF rewards chunks that are middling in *both* lists, so a chunk that is the best match
        # for one retriever (e.g. the exact keyword section) can be out-ranked by several
        # "okay everywhere" chunks and then dropped by the per-document cap. Guarantee the
        # lexical head (and, with a strong embedder, optionally the dense head) a place in the final k.
        heads = [i for i in lex_rank[:LEX_HEAD] if lex[i] > 0] + [i for i, _ in dense[:DENSE_HEAD]]
        parts = [p for p in COMPOUND.split(query) if len(p.split()) >= 3]
        if len(parts) > 1:      # compound question: each sub-question's best passage must reach the LLM
            for part in parts:
                sub = self._fuse(part)
                for h in sorted(sub, key=lambda i: -sub[i])[:SUB_HEADS]:
                    fused.setdefault(h, min(fused.values(), default=0.0))
                    if h not in heads:
                        heads.append(h)
        per_doc: dict[str, int] = {}
        picked: list[int] = []
        for i in ranked:
            if len(picked) == k:
                break
            d = self.chunks[i].doc_id
            if per_doc.get(d, 0) >= MAX_PER_DOC:
                continue
            per_doc[d] = per_doc.get(d, 0) + 1
            picked.append(i)
        # Add, never displace: swapping out the weakest pick traded one fix for a new miss (eval q23),
        # so guaranteed heads extend the context by at most max_extra passages.
        extra = 0
        for h in heads:
            if h in picked or h not in fused or extra >= max_extra:
                continue
            picked.append(h)
            extra += 1
        picked.sort(key=lambda i: -fused[i])

        top = fused[ranked[0]] if ranked else 1.0
        max_lex = max(lex) if lex else 0.0
        out: list[ScoredChunk] = [
            ScoredChunk(
                chunk=self.chunks[i],
                score=fused[i] / top,
                lexical_score=lex[i] / max_lex if max_lex else 0.0,
                dense_score=dense_sim.get(i, 0.0),
            )
            for i in picked
        ]
        rel = self.relevance(query, out)
        for s in out:
            s.raw_relevance = rel
        return out

    def _fuse(self, query: str) -> dict[int, float]:
        """RRF scores for one (sub-)query, used to find each sub-question's best passage."""
        lex = self.bm25.scores(query)
        lex_rank = sorted(range(len(self.chunks)), key=lambda i: -lex[i])[:CANDIDATES]
        dense = self.store.dense_search(self.embedder.embed([query])[0], CANDIDATES)
        fused: dict[int, float] = {}
        for r, i in enumerate(lex_rank):
            if lex[i] > 0:
                fused[i] = fused.get(i, 0.0) + self.lw / (RRF_K + r + 1)
        for r, (i, _) in enumerate(dense):
            fused[i] = fused.get(i, 0.0) + self.dw / (RRF_K + r + 1)
        return fused

    def relevance(self, query: str, results: list[ScoredChunk]) -> float:
        """Absolute answerability signal in [0, 1].

        Ranks alone can't say "nothing here is relevant"; this can. It combines
          (a) corpus coverage: share of the query's informative (idf-weighted) terms that exist
              anywhere in the corpus ('COBOL', 'blockchain' don't);
          (b) passage coverage: the best share of those terms found together in ONE of the top
              passages (an out-of-corpus question's words are scattered: 'travel' here, 'expense'
              there; a real answer's are co-located);
          (c) the best dense similarity.
        The threshold is tuned on the eval dev split only (see eval/README.md).
        """
        if not results:
            return 0.0
        coverage = self.bm25.query_coverage(query)
        passage = max(self.bm25.passage_coverage(query, r.chunk.embed_text) for r in results[:3])
        best_dense = max((r.dense_score for r in results), default=0.0)
        return 0.4 * coverage + 0.4 * passage + 0.2 * max(best_dense, 0.0)
