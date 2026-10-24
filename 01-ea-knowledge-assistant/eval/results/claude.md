# Evaluation results — `claude`

Run 2026-10-24 01:48 UTC · index `0da24c934d96e8fc` · 48 documents / 552 chunks · embedder `lsa` · answers `anthropic`
Test split: 29 answerable + 7 out-of-corpus questions (dev split of 14 used only to tune the not-found threshold = 0.51; lexical:dense fusion weight = 0.5:1).

## Retrieval (test split, answerable questions)

| Retriever | Hit@1 | Recall@5 | Precision@5 | MRR@10 |
|---|---|---|---|---|
| bm25_only | 79.3% | 100.0% | 59.3% | 0.880 |
| dense_only | 86.2% | 93.1% | 57.9% | 0.898 |
| hybrid_rrf (1:1) | 79.3% | 100.0% | 62.1% | 0.879 |
| hybrid_rrf (dev-tuned 0.5:1) | 86.2% | 100.0% | 62.1% | 0.910 |

## End to end (test split)

| Metric | Value |
|---|---|
| Answer passage reached the model (key fact in a retrieved passage from an expected document) | 89.7% |
| Answerable questions answered (not wrongly refused) | 96.6% |
| Out-of-corpus questions correctly refused ("not found") | 100.0% |
| Answer contains the key fact | 93.1% |
| Answer cites a relevant document | 89.7% |
| Claim support (factual sentences supported by the passage they cite) | 89.7% |
| Fully grounded answers (>= 90% of an answer's sentences cited and supported) | 67.9% |
| Every answer carries a citation | yes |
| Latency p50 / p95 | 3290 ms / 5301 ms |

## Failures

- `q18` expected **answer**, found=False, answer_in_context=False, cited=[]
- `q25` expected **answer**, found=True, answer_in_context=True, cited=['ADR-0036', 'ADR-0036', 'ADR-0036']
