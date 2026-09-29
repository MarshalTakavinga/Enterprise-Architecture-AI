"""Vector stores: in-memory (files on disk) for dev/CI, PostgreSQL + pgvector for deployment.

Both expose the same three operations: ``write`` (replace the index), ``load_chunks`` and
``dense_search``. The data model follows the spec: Document -> Chunk(embedding, section_ref).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .models import Chunk, Document


class InMemoryStore:
    def __init__(self, index_dir: Path):
        self.dir = index_dir
        self.chunks: list[Chunk] = []
        self.docs: dict[str, dict] = {}
        self.matrix: np.ndarray | None = None

    def write(self, docs: list[Document], chunks: list[Chunk], vectors: np.ndarray, meta: dict) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        (self.dir / "chunks.jsonl").write_text("\n".join(json.dumps(c.to_dict()) for c in chunks), encoding="utf-8")
        (self.dir / "documents.json").write_text(json.dumps([d.to_dict() for d in docs], indent=1), encoding="utf-8")
        np.save(self.dir / "vectors.npy", vectors)
        (self.dir / "meta.json").write_text(json.dumps(meta, indent=1))
        self.chunks, self.matrix = chunks, vectors
        self.docs = {d.doc_id: d.to_dict() for d in docs}

    def exists(self) -> bool:
        return (self.dir / "meta.json").exists()

    def meta(self) -> dict:
        return json.loads((self.dir / "meta.json").read_text())

    def load(self) -> None:
        self.chunks = [Chunk(**json.loads(l)) for l in (self.dir / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if l]
        self.docs = {d["doc_id"]: d for d in json.loads((self.dir / "documents.json").read_text(encoding="utf-8"))}
        self.matrix = np.load(self.dir / "vectors.npy")

    def load_chunks(self) -> list[Chunk]:
        return self.chunks

    def dense_search(self, qvec: np.ndarray, k: int) -> list[tuple[int, float]]:
        sims = self.matrix @ qvec
        idx = np.argsort(-sims)[:k]
        return [(int(i), float(sims[i])) for i in idx]


class PgVectorStore:
    """PostgreSQL + pgvector. Chosen over a dedicated vector DB for operational simplicity
    (one managed database for documents, chunks, vectors and the audit log) — see ADR-P002."""

    def __init__(self, dsn: str, index_dir: Path):
        import psycopg
        from pgvector.psycopg import register_vector

        self.conn = psycopg.connect(dsn, autocommit=True)
        self.conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        register_vector(self.conn)
        self.dir = index_dir
        self.chunks: list[Chunk] = []
        self.docs: dict[str, dict] = {}
        self._row_to_pos: dict[str, int] = {}

    def write(self, docs: list[Document], chunks: list[Chunk], vectors: np.ndarray, meta: dict) -> None:
        dim = vectors.shape[1]
        with self.conn.transaction():
            self.conn.execute("DROP TABLE IF EXISTS chunk; DROP TABLE IF EXISTS document; DROP TABLE IF EXISTS index_meta")
            self.conn.execute("""CREATE TABLE document (id text PRIMARY KEY, type text, title text, source_path text,
                                 version text, status text, owner text, effective_date text, meta jsonb)""")
            self.conn.execute(f"""CREATE TABLE chunk (id text PRIMARY KEY, document_id text REFERENCES document(id),
                                 ordinal int, section_ref text, heading_path text, text text, embedding vector({dim}))""")
            self.conn.execute("CREATE TABLE index_meta (k text PRIMARY KEY, v jsonb)")
            with self.conn.cursor() as cur:
                for d in docs:
                    cur.execute("INSERT INTO document VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                (d.doc_id, d.doc_type, d.title, d.source_path, d.version, d.status, d.owner,
                                 d.effective_date, json.dumps(d.to_dict())))
                for c, v in zip(chunks, vectors):
                    cur.execute("INSERT INTO chunk VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                (c.chunk_id, c.doc_id, c.ordinal, c.section_ref, c.heading_path, c.text, v))
                cur.execute("INSERT INTO index_meta VALUES ('meta', %s)", (json.dumps(meta),))
            # Exact search is fine at repository scale; add HNSW when chunks > ~50k.
            if len(chunks) > 50_000:
                self.conn.execute("CREATE INDEX ON chunk USING hnsw (embedding vector_cosine_ops)")
        self.load()

    def exists(self) -> bool:
        return self.conn.execute("SELECT to_regclass('index_meta') IS NOT NULL").fetchone()[0]

    def meta(self) -> dict:
        return self.conn.execute("SELECT v FROM index_meta WHERE k='meta'").fetchone()[0]

    def load(self) -> None:
        rows = self.conn.execute("""SELECT c.id, c.document_id, d.title, d.type, c.section_ref, c.text, c.ordinal, c.heading_path
                                    FROM chunk c JOIN document d ON d.id = c.document_id ORDER BY d.id, c.ordinal""").fetchall()
        self.chunks = [Chunk(chunk_id=r[0], doc_id=r[1], doc_title=r[2], doc_type=r[3], section_ref=r[4], text=r[5], ordinal=r[6], heading_path=r[7])
                       for r in rows]
        self._row_to_pos = {c.chunk_id: i for i, c in enumerate(self.chunks)}
        self.docs = {r[0]: r[1] for r in self.conn.execute("SELECT id, meta FROM document").fetchall()}

    def load_chunks(self) -> list[Chunk]:
        return self.chunks

    def dense_search(self, qvec: np.ndarray, k: int) -> list[tuple[int, float]]:
        rows = self.conn.execute(
            "SELECT id, 1 - (embedding <=> %s) AS sim FROM chunk ORDER BY embedding <=> %s LIMIT %s",
            (qvec, qvec, k)).fetchall()
        return [(self._row_to_pos[r[0]], float(r[1])) for r in rows]


def make_store(kind: str, index_dir: Path, dsn: str):
    if kind == "memory":
        return InMemoryStore(index_dir)
    if kind == "pgvector":
        return PgVectorStore(dsn, index_dir)
    raise ValueError(f"Unknown store: {kind}")
