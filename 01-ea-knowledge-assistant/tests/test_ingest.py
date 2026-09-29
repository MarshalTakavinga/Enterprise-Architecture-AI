from pathlib import Path

from eaka.ingest import build_chunks, chunk_document, load_corpus
from eaka.models import Document
from eaka.redact import redact

CORPUS = Path(__file__).resolve().parents[1] / "data" / "corpus"


def test_corpus_loads_with_unique_ids_and_metadata():
    docs = load_corpus(CORPUS)
    assert 40 <= len(docs) <= 60
    assert len({d.doc_id for d in docs}) == len(docs)
    types = {d.doc_type for d in docs}
    assert {"standard", "adr", "principle_catalog", "reference_architecture", "togaf_deliverable", "governance"} <= types
    for d in docs:
        assert d.title and d.version and d.owner, d.doc_id


def test_every_corpus_document_is_marked_synthetic():
    for p in CORPUS.rglob("*.md"):
        assert "fictional company" in p.read_text(encoding="utf-8")[:2500], p.name


def test_standard_clauses_are_individually_citable():
    docs = {d.doc_id: d for d in load_corpus(CORPUS)}
    refs = [c.section_ref for c in chunk_document(docs["STD-INT-001"])]
    assert any(r.startswith("§4.1 INT-P1") for r in refs)
    assert any(r.startswith("§4.2 INT-P2") for r in refs)


def test_principles_are_chunked_whole():
    docs = {d.doc_id: d for d in load_corpus(CORPUS)}
    chunks = chunk_document(docs["AP-CATALOG"])
    ap08 = [c for c in chunks if "AP-08" in c.section_ref]
    assert len(ap08) == 1
    assert "Statement" in ap08[0].text and "Implications" in ap08[0].text


def test_chunk_ids_unique_and_sizes_bounded():
    chunks = build_chunks(load_corpus(CORPUS))
    assert len({c.chunk_id for c in chunks}) == len(chunks)
    # Only single un-splittable blocks (big tables) may exceed the soft limit.
    assert sum(len(c.text.split()) > 420 for c in chunks) <= 6


def test_tables_are_not_split():
    doc = Document(doc_id="T-1", title="t", doc_type="standard", source_path="x",
                   body="## 1. Big\n\n" + "\n".join(f"| row {i} | " + "word " * 30 + "|" for i in range(30)))
    chunks = chunk_document(doc)
    assert len(chunks) == 1 and chunks[0].text.count("| row") == 30


def test_redaction():
    out = redact("Contact jane.doe@corp.com or +1 410 555 0199, api_key=abc123. Example: a.b@harbourline.example")
    assert "jane.doe" not in out and "555" not in out and "abc123" not in out
    assert "a.b@harbourline.example" in out   # RFC 2606 placeholder kept
    assert redact("Effective 2025-03-01, review 2026-03-01") == "Effective 2025-03-01, review 2026-03-01"
