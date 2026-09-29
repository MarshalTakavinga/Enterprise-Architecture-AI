# ADR-P003 — Pluggable LLM and embedding providers; Azure OpenAI recommended for Harbourline

**Status:** Accepted · **Date:** 2026-09-28 · **Decider:** Marshal Takavinga

## Context
The blueprint asks for one LLM provider, with the choice justified by data residency. Harbourline's
own standards settle the question for that organisation:
- **STD-AI-013** approves Azure OpenAI in approved regions as the LLM platform.
- **STD-DAT-005** requires EU personal data to stay in West Europe.

The portfolio, however, should run for any reviewer, with or without keys.

## Decision
- The code supports four answer providers: `extractive` (no LLM; the default), `azure_openai`,
  `anthropic` and `openai`.
- It supports four embedders: `lsa` (offline; the default), `azure_openai`, `openai` and
  `sentence_transformers` (local; no data leaves the host).
- **The recommended production configuration for Harbourline is Azure OpenAI deployed in the same
  region as the data.** Prompts carry repository text, which is classified Internal. In-region
  processing satisfies the organisation's own AI and residency standards without an exception.
- Anthropic and OpenAI stay available for reviewers and for organisations whose policies allow them.

## Consequences
- ✅ Runs anywhere offline, while the production story is explained by policy rather than preference.
- ⚠ Relevance thresholds depend on the embedder, so they must be re-tuned with `eval/run_eval.py`
  when the embedder changes. This is documented in `.env.example`.
