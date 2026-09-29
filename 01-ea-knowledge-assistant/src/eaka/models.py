"""Core data model: Document -> Chunk, plus retrieval and answer types."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Document:
    doc_id: str
    title: str
    doc_type: str
    source_path: str
    version: str = ""
    status: str = ""
    owner: str = ""
    effective_date: str = ""
    togaf_phase: str = ""
    related: list[str] = field(default_factory=list)
    body: str = ""

    def to_dict(self) -> dict:
        d = asdict(self)
        d.pop("body")
        return d


@dataclass
class Chunk:
    chunk_id: str          # e.g. "STD-INT-001#4.1"
    doc_id: str
    doc_title: str
    doc_type: str
    section_ref: str       # e.g. "§4.1 INT-P1 — Domain Event Publication"
    text: str              # section text as written (what gets quoted / cited)
    ordinal: int = 0
    heading_path: str = "" # e.g. "5 Topic Design › 5.1 Naming" (context for retrieval)

    @property
    def embed_text(self) -> str:
        """Text used for indexing: a contextual header makes short sections retrievable."""
        return f"{self.doc_id} {self.doc_title} ({self.doc_type}) — {self.heading_path or self.section_ref}\n{self.text}"

    @property
    def citation(self) -> str:
        return f"{self.doc_id} {self.section_ref}".strip()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ScoredChunk:
    chunk: Chunk
    score: float                      # fused, normalised to 0..1 (1 = best in this query)
    lexical_score: float = 0.0
    dense_score: float = 0.0
    raw_relevance: float = 0.0        # absolute relevance used for the not-found gate


@dataclass
class Citation:
    n: int
    doc_id: str
    title: str
    section_ref: str
    quote: str
    source_path: str = ""


@dataclass
class Answer:
    question: str
    answer: str
    found: bool
    citations: list[Citation] = field(default_factory=list)
    governance_notice: str | None = None
    grounded: bool | None = None       # result of the post-generation citation check
    provider: str = ""
    latency_ms: int = 0
    retrieved: list[str] = field(default_factory=list)  # chunk_ids, in rank order
    query_id: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
