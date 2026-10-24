"""Regression tests for passage-level retrieval failures found in the first LLM evaluation run.

Document-level Recall@5 was 100%, yet for these questions the section holding the answer never
reached the LLM, so Claude (correctly) replied NOT_FOUND. See eval/README.md.
"""
import pytest

from eaka.retrieval import COMPOUND, MAX_EXTRA


def _context(ka, question):
    # same call the answer pipeline makes (KnowledgeAssistant.ask)
    return [r.chunk.chunk_id for r in ka.retriever.search(question, k=ka.s.top_k, max_extra=MAX_EXTRA)]


def test_lexical_head_survives_fusion_and_doc_cap(ka):
    # BM25 ranks the naming section #1; RRF + the per-document cap used to drop it.
    assert "STD-EVT-003#5.1" in _context(ka, "How should we name Kafka topics?")


def test_compound_question_gets_a_passage_per_part(ka):
    ctx = _context(ka, "How long are application logs retained and can they contain personal data?")
    assert "STD-OBS-010#6" in ctx      # retention
    assert "STD-OBS-010#7" in ctx      # what must not be logged


@pytest.mark.parametrize("q,parts", [
    ("How long are logs retained and can they contain personal data?", 2),
    ("How do we version REST APIs and how much notice is required?", 2),
    ("What are the API and event standards?", 1),          # 'and' inside a noun phrase: no split
])
def test_compound_split(q, parts):
    assert len([p for p in COMPOUND.split(q) if len(p.split()) >= 3]) == parts


def test_plain_search_returns_exactly_k(ka):
    assert len(ka.retriever.search("What does ADR-0021 decide?", k=1)) == 1


@pytest.mark.parametrize("text,nums", [
    ("x [2]", [2]), ("x [1][3]", [1, 3]), ("x [1, 3]", [1, 3]),
    ("TLS 1.2 is the minimum [7, §4.1].", [7]),      # clause refs are not source numbers (eval q22)
    ("keys [3 §5]", [3]),
])
def test_cite_numbers(text, nums):
    from eaka.answer import cite_numbers
    assert cite_numbers(text) == nums
