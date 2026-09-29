# Governance & limitations

## What the assistant does, and what it deliberately does not do

| The assistant… | It does not… |
|---|---|
| Finds the principle, standard, ADR or deliverable that already answers a question and quotes it with a clause-level citation | Author, amend or interpret standards beyond what they say |
| Says "not found" when the repository doesn't cover a question, and logs the gap | Guess from general knowledge |
| Reports what the Exceptions Register and ADRs say about an exception, with a notice that the ARB decides | Grant, renew or judge an exception, or answer as if an exception's status were settled |
| Treats every corpus passage as data | Follow instructions found inside documents |

## Controls

| Risk | Control | Where |
|---|---|---|
| Hallucinated rules | Citation-forced prompt; `NOT_FOUND` path; post-generation groundedness check; answers without citations are converted to "not found" | `answer.py`, `engine.py` |
| Answering beyond the corpus | Relevance gate stops the request before any LLM call; threshold tuned on dev data | `retrieval.py`, `eval/` |
| Answers about governance exceptions | Notice added whenever the question or top evidence concerns an exception | `answer.mentions_exception` |
| Sensitive data entering the index | Ingestion-time redaction of emails, phone numbers, card numbers, keys and secrets; RFC 2606 placeholders kept | `redact.py` |
| Untraceable answers | Append-only audit log: question, answer, citations, retrieved chunks, grounding result, provider, latency, index version, caller | `querylog.py` |
| Stale index | Corpus + schema fingerprint; automatic re-index on change | `engine._stale` |
| Abuse or cost blow-up | API keys, per-caller rate limit, 2,000-character question cap, bounded context (6 passages) and output tokens | `api.py`, `config.py` |
| Data residency of prompts | Provider is configurable. Azure OpenAI in-region is the recommended choice for an organisation with EU and UAE residency rules (ADR-P003) | `answer.py`, `embeddings.py` |
| Prompt injection | The corpus is internal and curated, so the risk is low. Passages are still delimited, numbered and declared "not instructions" in the system prompt. Revisit if untrusted content, such as ARB submissions, is ever indexed (that is Project 9's problem) | `answer.SYSTEM_PROMPT` |

## Limitations

- **Synthetic corpus, single author.** The corpus and the evaluation questions were written together,
  so the numbers are best-case for this repository size. They are not a claim about production
  performance.
- **The offline dense model (LSA) is weak.** It is fitted on 552 chunks. Hosted or local neural
  embeddings are supported but have not been benchmarked here, because no key or model download was
  available in the build environment.
- **Retrieval-score gating can't catch everything.** It can't detect an out-of-corpus question whose
  every word appears in the corpus (for example "SAP S/4HANA upgrade timeline"). The LLM's `NOT_FOUND`
  instruction is the second line of defence. Extractive mode has no second line.
- **The groundedness check is lexical.** It catches invented facts and wrong citations, but it can't
  judge a subtle misreading of a correctly cited clause. Spot review by a human is still required (see
  eval/README.md).
- **No document-level access control.** Every indexed document is visible to every caller. A real
  deployment needs per-document classification filters, driven by the `classification` field in the
  front matter.
- **Point-in-time answers.** The assistant answers from the indexed versions of documents. It cannot
  know about decisions that haven't been written down, which is exactly what the gap log is for.
