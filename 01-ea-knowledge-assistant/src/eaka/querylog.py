"""Append-only audit log of every question and answer (governance requirement), plus the
"unanswered questions" log the EA Office uses to prioritise documentation gaps, and feedback."""
from __future__ import annotations

import json
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

from .models import Answer

_lock = threading.Lock()


class QueryLog:
    def __init__(self, log_dir: Path):
        self.dir = log_dir
        self.dir.mkdir(parents=True, exist_ok=True)
        self.audit = self.dir / "query_audit.jsonl"
        self.gaps = self.dir / "unanswered_questions.jsonl"
        self.feedback = self.dir / "feedback.jsonl"

    def _append(self, path: Path, record: dict) -> None:
        with _lock, path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def record(self, ans: Answer, user: str = "anonymous", index_version: str = "") -> str:
        qid = str(uuid.uuid4())
        rec = {
            "query_id": qid,
            "ts": datetime.now(timezone.utc).isoformat(),
            "user": user,
            "question": ans.question,
            "found": ans.found,
            "answer": ans.answer,
            "citations": [f"{c.doc_id} {c.section_ref}" for c in ans.citations],
            "retrieved": ans.retrieved,
            "grounded": ans.grounded,
            "governance_notice": bool(ans.governance_notice),
            "provider": ans.provider,
            "latency_ms": ans.latency_ms,
            "index_version": index_version,
        }
        self._append(self.audit, rec)
        if not ans.found:
            self._append(self.gaps, {k: rec[k] for k in ("query_id", "ts", "question", "retrieved")})
        return qid

    def record_feedback(self, query_id: str, correct: bool, comment: str = "", user: str = "anonymous") -> None:
        self._append(self.feedback, {"query_id": query_id, "ts": datetime.now(timezone.utc).isoformat(),
                                     "user": user, "correct": correct, "comment": comment[:2000]})
