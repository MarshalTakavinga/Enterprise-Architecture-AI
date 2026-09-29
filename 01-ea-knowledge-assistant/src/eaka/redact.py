"""Ingestion-time redaction of sensitive values that should never enter the index.

The architecture corpus should not contain personal or secret data; this is a safety net
for when it accidentally does (governance requirement in the project spec).
"""
from __future__ import annotations

import re

PATTERNS: list[tuple[str, re.Pattern]] = [
    ("EMAIL", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("PHONE", re.compile(r"(?<![\w-])\+?\d{1,3}[ .-]?\(?\d{2,4}\)?[ .-]\d{3,4}[ .-]\d{3,4}(?![\w-])")),
    ("SECRET", re.compile(r"(?i)\b(?:api[_-]?key|secret|password|pwd|token)\s*[:=]\s*\S+")),
    ("AWS_KEY", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("CARD", re.compile(r"\b(?:\d[ -]?){13,16}\b")),
]


# RFC 2606 reserved names are documentation placeholders, never real addresses.
RESERVED = re.compile(r"(?i)\.(example|test|invalid)$|@example\.(com|org|net)$")


def redact(text: str) -> str:
    for label, pat in PATTERNS:
        text = pat.sub(lambda m: m.group(0) if label == "EMAIL" and RESERVED.search(m.group(0))
                       else f"[REDACTED-{label}]", text)
    return text
