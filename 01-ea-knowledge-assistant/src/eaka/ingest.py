"""Load the architecture repository and split it into citable chunks.

Chunking is document-type aware (blueprint Phase 3):
  * principle_catalog -> one chunk per principle (Statement/Rationale/Implications stay together,
    because a principle quoted without its implications is misleading)
  * adr -> one chunk per top-level section (Context, Drivers, Options, Outcome, ...)
  * everything else -> one chunk per deepest numbered section (so a standard's clause
    can be cited as e.g. "STD-INT-001 §4.1")
Oversized sections are split on paragraph boundaries; tables and code blocks are never split.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

import yaml

from .models import Chunk, Document
from .redact import redact

FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
HEADING = re.compile(r"^(#{1,4})\s+(.*)$")
NUMBERED = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")

INDEX_SCHEMA = "4"  # bump when chunking/tokenisation changes so indexes rebuild automatically
MAX_WORDS = 420
MIN_WORDS = 25
# Level at which each doc type is chunked (2 = "##", 3 = "###").
CHUNK_LEVEL = {"principle_catalog": 2, "adr": 2}
DEFAULT_LEVEL = 3


def load_document(path: Path) -> Document:
    raw = path.read_text(encoding="utf-8")
    m = FRONT_MATTER.match(raw)
    meta = yaml.safe_load(m.group(1)) if m else {}
    body = raw[m.end():] if m else raw
    body = redact(body)
    doc_id = str(meta.get("doc_id") or path.stem)
    return Document(
        doc_id=doc_id,
        title=str(meta.get("title", path.stem)),
        doc_type=str(meta.get("doc_type", "document")),
        source_path=str(path),
        version=str(meta.get("version", "")),
        status=str(meta.get("status", "")),
        owner=str(meta.get("owner", "")),
        effective_date=str(meta.get("effective_date", "")),
        togaf_phase=str(meta.get("togaf_phase", "") or ""),
        related=[str(r) for r in (meta.get("related") or [])],
        body=body,
    )


def load_corpus(corpus_dir: Path) -> list[Document]:
    docs = [load_document(p) for p in sorted(corpus_dir.rglob("*.md"))]
    ids = [d.doc_id for d in docs]
    dupes = {i for i in ids if ids.count(i) > 1}
    if dupes:
        raise ValueError(f"Duplicate doc_id(s) in corpus: {sorted(dupes)}")
    return docs


def _section_ref(heading: str) -> tuple[str, str]:
    """'4.1 INT-P1 — Domain Event Publication' -> ('4.1', '§4.1 INT-P1 — Domain Event Publication')."""
    m = NUMBERED.match(heading.strip())
    if m:
        return m.group(1), f"§{m.group(1)} {m.group(2).strip()}"
    return "", heading.strip()


def _split_blocks(text: str) -> list[str]:
    """Paragraph blocks, keeping tables, lists and fenced code together."""
    blocks, cur, in_fence = [], [], False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        if not line.strip() and not in_fence:
            if cur:
                blocks.append("\n".join(cur))
                cur = []
            continue
        cur.append(line)
    if cur:
        blocks.append("\n".join(cur))
    return blocks


def _words(s: str) -> int:
    return len(s.split())


def _split_oversized(text: str) -> list[str]:
    if _words(text) <= MAX_WORDS:
        return [text]
    parts, cur = [], []
    for block in _split_blocks(text):
        if cur and _words("\n\n".join(cur + [block])) > MAX_WORDS:
            parts.append("\n\n".join(cur))
            # one-block overlap keeps the lead-in sentence for context
            cur = [cur[-1]] if _words(cur[-1]) < 80 else []
        cur.append(block)
    if cur:
        parts.append("\n\n".join(cur))
    return parts


def chunk_document(doc: Document) -> list[Chunk]:
    level = CHUNK_LEVEL.get(doc.doc_type, DEFAULT_LEVEL)
    sections: list[tuple[list[str], list[str]]] = []  # (heading path, lines)
    path: list[str] = []
    cur_lines: list[str] = []
    in_fence = False

    def flush():
        if any(l.strip() for l in cur_lines):
            sections.append((list(path), list(cur_lines)))

    for line in doc.body.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        m = HEADING.match(line) if not in_fence else None
        if m and 2 <= len(m.group(1)) <= level:
            flush()
            cur_lines = []
            depth = len(m.group(1)) - 2  # "##" -> 0
            path = path[:depth] + [m.group(2).strip()]
            continue
        if m and len(m.group(1)) == 1:
            continue  # document title line; carried in metadata
        cur_lines.append(line)
    flush()

    # Merge tiny sections (e.g. a one-line "Status") into the following section.
    merged: list[tuple[list[str], str]] = []
    carry = ""
    for hpath, lines in sections:
        text = "\n".join(lines).strip()
        text = re.sub(r"^>\s*Synthetic document.*$", "", text, flags=re.M).strip()
        if not text:
            continue
        if carry:
            text = carry + "\n\n" + text
            carry = ""
        if _words(text) < MIN_WORDS and hpath:
            carry = f"**{hpath[-1]}**\n{text}"
            continue
        merged.append((hpath, text))
    if carry and merged:
        hp, t = merged[-1]
        merged[-1] = (hp, t + "\n\n" + carry)
    elif carry:
        merged.append(([], carry))

    chunks: list[Chunk] = []
    for hpath, text in merged:
        if hpath:
            num, ref = _section_ref(hpath[-1])
            if len(hpath) > 1 and not num:
                ref = f"{_section_ref(hpath[0])[1]} › {ref}"
        else:
            num, ref = "", "Preamble"
        for part_i, part in enumerate(_split_oversized(text)):
            suffix = f" (part {part_i + 1})" if part_i else ""
            key = num or hashlib.sha1(ref.encode()).hexdigest()[:6]
            chunks.append(Chunk(
                chunk_id=f"{doc.doc_id}#{key}{'-' + str(part_i + 1) if part_i else ''}",
                doc_id=doc.doc_id,
                doc_title=doc.title,
                doc_type=doc.doc_type,
                section_ref=ref + suffix,
                text=part.strip(),
                ordinal=len(chunks),
                heading_path=" › ".join(hpath),
            ))
    # Guarantee unique ids even for repeated unnumbered headings.
    seen: dict[str, int] = {}
    for c in chunks:
        if c.chunk_id in seen:
            seen[c.chunk_id] += 1
            c.chunk_id = f"{c.chunk_id}~{seen[c.chunk_id]}"
        else:
            seen[c.chunk_id] = 0
    return chunks


def build_chunks(docs: list[Document]) -> list[Chunk]:
    out: list[Chunk] = []
    for d in docs:
        out.extend(chunk_document(d))
    return out


def corpus_fingerprint(corpus_dir: Path) -> str:
    """Hash of every file's path + content; used to re-index only when the corpus changed."""
    h = hashlib.sha256(INDEX_SCHEMA.encode())
    for p in sorted(corpus_dir.rglob("*.md")):
        h.update(str(p.relative_to(corpus_dir)).encode())
        h.update(p.read_bytes())
    return h.hexdigest()[:16]
