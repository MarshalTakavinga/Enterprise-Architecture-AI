# Evaluation results — `offline_baseline`

Run 2026-09-29 01:22 UTC · index `0c4b3ecf6470b732` · 48 documents / 552 chunks · embedder `lsa` · answers `extractive`
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
| Answerable questions answered (not wrongly refused) | 100.0% |
| Out-of-corpus questions correctly refused ("not found") | 85.7% |
| Answer contains the key fact | 72.4% |
| Answer cites a relevant document | 96.6% |
| Groundedness (answers whose claims are supported by their citations) | 100.0% |
| Every answer carries a citation | yes |
| Latency p50 / p95 | 31 ms / 39 ms |

## Failures

- `q04` expected **answer**, found=True, cited=['STD-EVT-003', 'STD-EVT-003', 'STD-DAT-004', 'STD-EVT-003']
- `q08` expected **answer**, found=True, cited=['ADR-0030', 'ADR-0030', 'ADR-0030', 'ADD-01']
- `q18` expected **answer**, found=True, cited=['RA-04', 'ADR-0012', 'STD-DAT-005', 'STD-INT-001', 'STD-INT-001']
- `q19` expected **answer**, found=True, cited=['STD-CTR-012', 'STD-IAM-008', 'AP-CATALOG']
- `q22` expected **answer**, found=True, cited=['STD-DAT-004', 'STD-SEC-009', 'STD-SEC-009', 'STD-DAT-004']
- `q27` expected **answer**, found=True, cited=['STD-OBS-010', 'STD-DAT-004', 'STD-API-002']
- `q31` expected **answer**, found=True, cited=['STD-AI-013', 'STD-AI-013', 'STD-AI-013']
- `q34` expected **answer**, found=True, cited=['GOV-02', 'ADD-01', 'PRE-02', 'A-01']
- `n09` expected **not_found**, found=True, cited=['PRE-02', 'A-01', 'A-02', 'PRE-02', 'G-01']
