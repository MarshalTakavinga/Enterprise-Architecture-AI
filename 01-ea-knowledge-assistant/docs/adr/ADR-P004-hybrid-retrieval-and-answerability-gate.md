# ADR-P004 — Hybrid retrieval with an answerability gate

**Status:** Accepted · **Date:** 2026-09-28 · **Decider:** Marshal Takavinga

## Context
Architecture questions mix exact identifiers ("does ADR-0021 still apply?", "INT-P2") with loose
paraphrase ("can my service read another team's database?"). The assistant also has to refuse
questions the corpus doesn't cover, and rank scores alone can't do that because the top result is
always "the best of what's there".

## Decision
1. **BM25 + dense retrieval fused with Reciprocal Rank Fusion**, plus a boost for document IDs named
   in the question. The fusion weight is chosen on the eval dev split.
2. **An answerability score** combining three signals:
   - corpus coverage of the query's informative terms;
   - co-location of those terms in one passage;
   - dense similarity.

   The threshold is the max-margin point between answerable and out-of-corpus questions on the dev
   split. Below it, the assistant says "not found" **before** any LLM call.
3. **A second gate:** the LLM must answer `NOT_FOUND` when the passages don't contain the answer.

## Evidence (test split, offline configuration — eval/results/offline_baseline.md)
| Retriever | Hit@1 | Recall@5 | MRR@10 |
|---|---|---|---|
| BM25 only | 79.3% | 100% | 0.880 |
| Dense (LSA) only | 86.2% | 93.1% | 0.898 |
| **Hybrid, dev-tuned** | **86.2%** | **100%** | **0.910** |

The gate refused 6 of 7 out-of-corpus test questions and wrongly refused none of the 29 answerable
ones.

## Consequences
- ✅ Cheaper and safer: most unanswerable questions never reach the LLM.
- ⚠ The gate can't catch questions whose vocabulary is fully in the corpus. The LLM gate covers
  that case.
- ⚠ The threshold must be re-tuned when the embedder or corpus changes significantly.
