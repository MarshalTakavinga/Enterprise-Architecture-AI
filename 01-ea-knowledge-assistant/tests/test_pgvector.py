"""Integration test for the PostgreSQL + pgvector store. Skipped unless EAKA_TEST_DATABASE_URL is set
(CI provides a pgvector service container)."""
import os
from dataclasses import replace

import pytest

DSN = os.environ.get("EAKA_TEST_DATABASE_URL")
pytestmark = [pytest.mark.pgvector, pytest.mark.skipif(not DSN, reason="EAKA_TEST_DATABASE_URL not set")]


def test_pgvector_store_matches_memory_store(settings, ka):
    from eaka.engine import KnowledgeAssistant

    pg = KnowledgeAssistant(replace(settings, store="pgvector", database_url=DSN,
                                    index_dir=settings.index_dir.parent / "pg-index"))
    assert pg.meta["chunks"] == ka.meta["chunks"]
    q = "Are we allowed to use a NoSQL database?"
    mem_top = [r.chunk.chunk_id for r in ka.retriever.search(q, k=5)]
    pg_top = [r.chunk.chunk_id for r in pg.retriever.search(q, k=5)]
    assert mem_top[:3] == pg_top[:3]
    assert pg.ask(q, log=False).found
