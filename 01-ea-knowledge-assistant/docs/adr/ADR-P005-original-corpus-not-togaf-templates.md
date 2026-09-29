# ADR-P005 — Write an original corpus instead of filling The Open Group's TOGAF templates

**Status:** Accepted · **Date:** 2026-09-28 · **Decider:** Marshal Takavinga

## Context
The TOGAF® Standard, 10th Edition template deliverables were available locally. Filling them with a
realistic example looked like the fastest way to a realistic corpus. Their licence, however, prohibits
using the documents in connection with generative AI systems "to generate any data or content and/or
to synthesize or combine with any other data or content" without written permission. It also requires
copyright notices to be retained on every copy. Indexing them in a RAG system, or publishing filled
copies on GitHub, would breach those terms.

## Decision
Write **original** documents for a fictional enterprise, Harbourline Logistics Group. These documents
follow the TOGAF ADM deliverable *names* and the generic structure an architect would recognise:
- Request for Architecture Work, Architecture Vision, Statement of Architecture Work;
- Architecture Definition Document, Architecture Requirements Specification;
- Roadmap & Migration Plan, Architecture Contract, Compliance Assessment;
- Change Request, Requirements Impact Assessment;
- principles written as Name / Statement / Rationale / Implications.

No Open Group text is used. The template files remain local only and are excluded from Git by
`.gitignore`.

## Consequences
- ✅ The portfolio is safe to publish, and the content shows the author's own architecture judgement
  rather than a template.
- ✅ One consistent fictional enterprise, recorded in `data/WORLD_BIBLE.md`, can be reused by
  Projects 2–10.
- ⚠ The documents are not formally "TOGAF template deliverables". They are described as following the
  ADM deliverable structure.
