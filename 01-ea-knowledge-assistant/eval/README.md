# Evaluation

`queries.yaml` holds **50 hand-labelled questions**: 40 answerable from the corpus and 10 deliberately
**out of corpus** (mainframe, blockchain, travel policy, salary bands and similar topics that the corpus
was written never to mention). The answerable questions are paraphrased the way an architect would ask
them, not copied from section headings.

The set is split so that no reported number is tuned on the data it's reported on:

| Split | Size | Used for |
|---|---|---|
| dev | 14 (11 answerable, 3 out of corpus) | choosing the lexical:dense fusion weight (best MRR) and the not-found threshold (max-margin between the two classes) |
| test | 36 (29 answerable, 7 out of corpus) | every number in `results/` |

Before scoring, a **label sanity check** confirms that every labelled document exists and that the
primary one actually contains the expected answer keyword.

## Metrics

| Metric | Meaning |
|---|---|
| Hit@1, Recall@5, Precision@5, MRR@10 | Retrieval quality. A retrieved chunk counts as relevant if it comes from a labelled document. Recall@5 is the share of questions with at least one relevant chunk in the top 5. |
| Answerable answered | Share of answerable questions the gate did *not* wrongly refuse. |
| Out-of-corpus refused | Share of out-of-corpus questions answered with "not found" instead of a guess. |
| Answer contains key fact | The answer text includes the labelled key fact (for example "West Europe" or "2025-06-30"). |
| Groundedness | Share of answers whose every claim sentence cites a valid source and shares at least 50% of its content words with that source (`eaka.answer.check_groundedness`). |
| Latency p50/p95 | End to end, measured in-process. |

## Results so far

[`results/offline_baseline.md`](results/offline_baseline.md) uses the offline configuration: BM25 + LSA
hybrid retrieval with extractive answers and no API keys. On the test split:

- **Recall@5 is 100%, MRR is 0.910 and Hit@1 is 86%** with the dev-tuned hybrid retriever. Hybrid
  retrieval beats BM25-only on MRR (0.880) and beats dense-only on recall (93%).
- **86% of out-of-corpus questions are refused.** The one miss, "SAP S/4HANA version upgrade
  timeline", uses only words that do appear in the corpus. A retrieval-score gate cannot catch that
  kind of question. Catching it is the job of the second gate: the LLM's `NOT_FOUND` rule.
- **The key fact appears in 72% of answers.** Extractive mode can only quote whole sentences, so it
  often quotes a sentence *about* the rule rather than the one containing the number. This is the gap
  that LLM synthesis is meant to close.
- **Groundedness is 100% in extractive mode, but only because it holds by construction** (the answer
  is quoted text). It is not evidence about LLM behaviour.

## Still to measure

Run the evaluation with an LLM to get the numbers that matter most for generated answers:

```bash
EAKA_LLM_PROVIDER=anthropic ANTHROPIC_API_KEY=... python eval/run_eval.py --tag claude
EAKA_LLM_PROVIDER=azure_openai AZURE_OPENAI_API_KEY=... AZURE_OPENAI_ENDPOINT=... AZURE_OPENAI_DEPLOYMENT=... python eval/run_eval.py --tag azure-openai
```

If you also switch the embedder (for example `EAKA_EMBEDDER=azure_openai`), the relevance scale
changes. In that case read the dev-tuned threshold and weight off the new report and set
`EAKA_MIN_RELEVANCE` and `EAKA_LEXICAL_WEIGHT` to match.

## Honest limitations

- **The labels are small and were written by one person.** 50 questions give indicative numbers,
  not statistically tight ones. The 👍/👎 feedback in the UI (`logs/feedback.jsonl`) is how the set
  is meant to grow.
- **Corpus and questions share an author.** A real repository written by many people would be
  messier, and retrieval scores would be lower.
