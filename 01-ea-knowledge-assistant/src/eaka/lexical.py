"""BM25 keyword retrieval.

Architecture questions are full of exact identifiers (STD-DB-006, ADR-0030, INT-P2, Cosmos DB,
EXC-2025-003) that dense embeddings blur; BM25 catches them. It is fused with the dense
ranking in ``retrieval.py``.
"""
from __future__ import annotations

import math
import re
from collections import Counter
from functools import lru_cache

import snowballstemmer

_STEMMER = snowballstemmer.stemmer("english")


@lru_cache(maxsize=50_000)
def stem(token: str) -> str:
    """Snowball-stem plain words ('deprecating'/'deprecation' -> 'deprec'); leave IDs untouched."""
    return _STEMMER.stemWord(token) if token.isalpha() else token

TOKEN = re.compile(r"[a-z0-9]+(?:[-.][a-z0-9]+)*")
STOP = set("""a an the and or of to in on for with by is are was be been it its this that as at from
which what when where who how do does did done can could would may must should we our you your
i me my any all there their they them not no yes if than then so into about over under someone
anyone something anything""".split())


def tokenize(text: str) -> list[str]:
    toks = []
    for t in TOKEN.findall(text.lower()):
        if t in STOP:
            continue
        toks.append(stem(t))
        if "-" in t or "." in t:          # index "std-db-006" as well as "std", "db", "006"
            toks.extend(stem(p) for p in re.split(r"[-.]", t) if p and p not in STOP)
    return toks


class BM25:
    def __init__(self, k1: float = 1.4, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs: list[Counter] = []
        self.df: Counter = Counter()
        self.lens: list[int] = []
        self.avgdl = 0.0

    def fit(self, texts: list[str]) -> "BM25":
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avgdl = sum(self.lens) / max(len(self.lens), 1)
        self.df = Counter()
        for d in self.docs:
            self.df.update(d.keys())
        return self

    def idf(self, term: str) -> float:
        n = len(self.docs)
        df = self.df.get(term, 0)
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def scores(self, query: str) -> list[float]:
        q = tokenize(query)
        out = []
        for d, dl in zip(self.docs, self.lens):
            s = 0.0
            for t in q:
                f = d.get(t, 0)
                if f:
                    s += self.idf(t) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avgdl))
            out.append(s)
        return out

    def _weights(self, query: str) -> dict[str, float]:
        n = len(self.docs)
        unseen_idf = math.log(1 + (n + 0.5) / 0.5)
        return {t: (self.idf(t) if t in self.df else unseen_idf)
                for t in dict.fromkeys(tokenize(query)) if len(t) > 2}

    def passage_coverage(self, query: str, passage: str) -> float:
        """Idf-weighted share of the query's terms that appear in one passage."""
        w = self._weights(query)
        total = sum(w.values())
        if not total:
            return 0.0
        toks = set(tokenize(passage))
        return sum(v for t, v in w.items() if t in toks) / total

    def query_coverage(self, query: str) -> float:
        """Share of the query's informative (idf-weighted) terms that exist anywhere in the corpus.

        Used by the not-found gate: a question whose key terms never appear in the corpus
        (e.g. 'COBOL', 'blockchain') is almost certainly not answerable from it.
        """
        q = [t for t in dict.fromkeys(tokenize(query)) if len(t) > 2]
        if not q:
            return 0.0
        n = len(self.docs)
        unseen_idf = math.log(1 + (n + 0.5) / 0.5)
        total = sum(self.idf(t) if t in self.df else unseen_idf for t in q)
        seen = sum(self.idf(t) for t in q if t in self.df)
        return seen / total if total else 0.0
