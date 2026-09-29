"""FastAPI backend.

    uvicorn eaka.api:app --reload

Auth: when EAKA_API_KEYS is set, every endpoint except /health requires an ``X-API-Key`` header.
In a real deployment this sits behind Entra ID / APIM (STD-IAM-008, STD-API-002 in the corpus);
the key check is the minimum control for a portfolio deployment.
"""
from __future__ import annotations

import time
from collections import defaultdict, deque
from functools import lru_cache

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field

from .config import get_settings
from .engine import KnowledgeAssistant

app = FastAPI(title="EA Knowledge Assistant", version="1.0.0",
              description="Cited answers from the Harbourline architecture repository (synthetic).")


@lru_cache(maxsize=1)
def assistant() -> KnowledgeAssistant:
    return KnowledgeAssistant()


_hits: dict[str, deque] = defaultdict(deque)


def guard(request: Request, x_api_key: str | None = Header(default=None)) -> str:
    s = get_settings()
    if s.api_keys and x_api_key not in s.api_keys:
        raise HTTPException(status_code=401, detail="Missing or invalid X-API-Key")
    caller = x_api_key or (request.client.host if request.client else "unknown")
    now, window = time.monotonic(), _hits[caller]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= s.rate_limit_per_minute:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    window.append(now)
    return f"key:{x_api_key[:4]}…" if x_api_key else caller


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)


class FeedbackRequest(BaseModel):
    query_id: str
    correct: bool
    comment: str = Field(default="", max_length=2000)


@app.get("/health")
def health() -> dict:
    a = assistant()
    return {"status": "ok", "documents": a.meta.get("documents"), "chunks": a.meta.get("chunks"),
            "embedder": a.meta.get("embedder"), "index_version": a.meta.get("corpus_fingerprint")}


@app.post("/ask")
def ask(req: AskRequest, caller: str = Depends(guard)) -> dict:
    return assistant().ask(req.question, user=caller).to_dict()


@app.get("/documents")
def documents(doc_type: str | None = None, caller: str = Depends(guard)) -> list[dict]:
    docs = assistant().documents.values()
    return sorted((d for d in docs if not doc_type or d["doc_type"] == doc_type), key=lambda d: d["doc_id"])


@app.get("/documents/{doc_id}")
def document(doc_id: str, caller: str = Depends(guard)) -> dict:
    d = assistant().documents.get(doc_id)
    if not d:
        raise HTTPException(status_code=404, detail="Unknown document")
    return d


@app.post("/feedback")
def feedback(req: FeedbackRequest, caller: str = Depends(guard)) -> dict:
    assistant().log.record_feedback(req.query_id, req.correct, req.comment, user=caller)
    return {"status": "recorded"}
