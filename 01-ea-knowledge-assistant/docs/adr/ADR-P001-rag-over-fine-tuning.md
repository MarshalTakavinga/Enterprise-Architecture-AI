# ADR-P001 — Retrieval-augmented generation, not fine-tuning

**Status:** Accepted · **Date:** 2026-09-28 · **Decider:** Marshal Takavinga

## Context
Architects need answers that match the *current* approved version of a standard, together with a
citation they can check. The repository changes every week: ADRs are added, standards are revised and
exceptions expire.

## Options
1. **Fine-tune an LLM on the repository.** The knowledge is baked into the model weights. The model
   can't cite a clause, has to be retrained on every change, and there's no way to show which document
   produced an answer.
2. **Long-context prompting with the whole repository** (~66k words ≈ 90k tokens). This is feasible at
   the current size, but every question costs the full corpus in tokens, it doesn't scale to a real
   repository of thousands of documents, and attributing a citation to a precise clause is weaker.
3. **RAG.** Retrieve the few relevant clauses, answer only from them and cite them.

## Decision
Option 3, **RAG**.

## Consequences
- ✅ Answers track the corpus on the next re-index, with no retraining.
- ✅ Every answer is traceable to document and clause, which the governance model requires.
- ✅ The corpus can say "not found", which a fine-tuned model can't do reliably.
- ⚠ Answer quality is capped by retrieval quality, so retrieval is evaluated separately (eval/).
- ⚠ The chunking design matters, and it is type-aware (see architecture.md).
