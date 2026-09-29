"""Evaluate retrieval, not-found behaviour, answer correctness, groundedness and latency.

    python eval/run_eval.py                      # offline: hybrid BM25+LSA, extractive answers
    EAKA_LLM_PROVIDER=anthropic python eval/run_eval.py --tag claude   # with an LLM

Writes eval/results/<tag>.json and eval/results/<tag>.md.
The not-found threshold is tuned on the *dev* split only; headline numbers are the *test* split.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from dataclasses import replace
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eaka.answer import check_groundedness, generate  # noqa: E402
from eaka.config import get_settings  # noqa: E402
from eaka.engine import KnowledgeAssistant  # noqa: E402
from eaka.retrieval import Retriever  # noqa: E402

K = 5


def load_queries() -> list[dict]:
    qs = yaml.safe_load((ROOT / "eval" / "queries.yaml").read_text())["queries"]
    for q in qs:
        q.setdefault("expect", "answer")
    return qs


def label_sanity(ka: KnowledgeAssistant, qs: list[dict]) -> list[str]:
    """Every relevant doc must exist and the primary one must contain an answer keyword."""
    problems = []
    text_by_doc: dict[str, str] = {}
    for c in ka.retriever.chunks:
        text_by_doc[c.doc_id] = text_by_doc.get(c.doc_id, "") + "\n" + c.text.lower()
    for q in qs:
        if q["expect"] != "answer":
            continue
        for d in q["relevant_docs"]:
            if d not in text_by_doc:
                problems.append(f"{q['id']}: unknown doc {d}")
        alts = [a.lower() for kw in q["answer_keywords"] for a in kw.split("|")]
        if not any(a in text_by_doc.get(q["relevant_docs"][0], "") for a in alts):
            problems.append(f"{q['id']}: primary doc {q['relevant_docs'][0]} lacks answer keyword")
    return problems


def retrieval_metrics(retriever: Retriever, qs: list[dict]) -> dict:
    hit1 = hit5 = prec = rr = 0.0
    n = 0
    per_query = {}
    for q in qs:
        if q["expect"] != "answer":
            continue
        n += 1
        res = retriever.search(q["question"], k=10)
        rel = [r.chunk.doc_id in q["relevant_docs"] for r in res]
        hit1 += rel[0] if rel else 0
        hit5 += any(rel[:K])
        prec += sum(rel[:K]) / K
        first = next((i for i, x in enumerate(rel) if x), None)
        rr += 1 / (first + 1) if first is not None else 0
        per_query[q["id"]] = [r.chunk.chunk_id for r in res[:K]]
    return {"n": n, "hit@1": hit1 / n, "recall@5": hit5 / n, "precision@5": prec / n, "mrr@10": rr / n,
            "top5": per_query}


def tune_threshold(retriever: Retriever, dev: list[dict]) -> tuple[float, list]:
    """Pick the not-found threshold on the dev split: maximise balanced accuracy, then take the
    middle of the widest gap between answerable and out-of-corpus scores (max-margin), so the
    boundary isn't hugging either class."""
    scores = sorted((retriever.search(q["question"], k=6)[0].raw_relevance, q["expect"]) for q in dev)
    pos = sum(1 for _, e in scores if e == "answer")
    neg = len(scores) - pos
    cands = [0.0] + [(scores[i][0] + scores[i + 1][0]) / 2 for i in range(len(scores) - 1)] + [1.0]

    def bal(t):
        tp = sum(1 for s, e in scores if e == "answer" and s >= t)
        tn = sum(1 for s, e in scores if e == "not_found" and s < t)
        return 0.5 * (tp / pos + tn / neg)

    best = max(bal(t) for t in cands)
    good = [i for i in range(len(scores) - 1) if abs(bal(cands[i + 1]) - best) < 1e-9]
    i = max(good, key=lambda i: scores[i + 1][0] - scores[i][0])
    return round(cands[i + 1], 3), [(round(s, 3), e) for s, e in scores]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default=None)
    args = ap.parse_args()

    s = get_settings()
    ka = KnowledgeAssistant(s)
    qs = load_queries()
    problems = label_sanity(ka, qs)
    dev = [q for q in qs if q["split"] == "dev"]
    test = [q for q in qs if q["split"] == "test"]

    # 1. Retrieval. Fusion weight tuned on dev (MRR), then all variants reported on test.
    dev_mrr = {}
    for lw in (0.5, 1.0, 1.5, 2.0, 3.0):
        dev_mrr[lw] = retrieval_metrics(Retriever(ka.store, ka.embedder, lexical_weight=lw), dev)["mrr@10"]
    best_lw = max(dev_mrr, key=lambda w: (round(dev_mrr[w], 4), -abs(w - 1.0)))
    configs = {"bm25_only": (1.0, 0.0), "dense_only": (0.0, 1.0), "hybrid_rrf (1:1)": (1.0, 1.0),
               f"hybrid_rrf (dev-tuned {best_lw}:1)": (best_lw, 1.0)}
    retrieval = {}
    for name, (lw, dw) in configs.items():
        r = Retriever(ka.store, ka.embedder, lexical_weight=lw, dense_weight=dw)
        retrieval[name] = retrieval_metrics(r, test)

    # 2. Not-found threshold tuned on dev, applied to test.
    threshold, dev_scores = tune_threshold(Retriever(ka.store, ka.embedder, lexical_weight=best_lw), dev)
    ka.s = replace(ka.s, min_relevance=threshold, lexical_weight=best_lw)
    ka.retriever = Retriever(ka.store, ka.embedder, lexical_weight=best_lw)

    # 3. End-to-end on test.
    rows, latencies = [], []
    for q in test:
        t0 = time.perf_counter()
        ans = ka.ask(q["question"], user="eval", log=False)
        latencies.append((time.perf_counter() - t0) * 1000)
        row = {"id": q["id"], "expect": q["expect"], "found": ans.found, "grounded": ans.grounded,
               "citations": [c.doc_id for c in ans.citations]}
        if q["expect"] == "answer":
            alts = [[a.lower() for a in kw.split("|")] for kw in q["answer_keywords"]]
            row["keywords_ok"] = ans.found and all(any(a in ans.answer.lower() for a in kw) for kw in alts)
            row["cites_relevant"] = any(d in q["relevant_docs"] for d in row["citations"])
        rows.append(row)

    ans_rows = [r for r in rows if r["expect"] == "answer"]
    nf_rows = [r for r in rows if r["expect"] == "not_found"]
    found_rows = [r for r in rows if r["found"]]
    e2e = {
        "answerable_answered": sum(r["found"] for r in ans_rows) / len(ans_rows),
        "out_of_corpus_refused": sum(not r["found"] for r in nf_rows) / len(nf_rows),
        "answer_contains_key_fact": sum(r["keywords_ok"] for r in ans_rows) / len(ans_rows),
        "answer_cites_relevant_doc": sum(r["cites_relevant"] for r in ans_rows) / len(ans_rows),
        "groundedness_rate": (sum(bool(r["grounded"]) for r in found_rows) / len(found_rows)) if found_rows else None,
        "every_answer_cited": all(r["citations"] for r in found_rows),
        "latency_ms_p50": statistics.median(latencies),
        "latency_ms_p95": sorted(latencies)[max(0, int(0.95 * len(latencies)) - 1)],
    }

    tag = args.tag or f"{ka.meta['embedder'].split(':')[0]}_{s.llm_provider}"
    out = {
        "tag": tag, "run_at": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()),
        "index": ka.meta, "llm_provider": s.llm_provider, "k": K,
        "queries": {"dev": len(dev), "test": len(test),
                    "test_answerable": len(ans_rows), "test_out_of_corpus": len(nf_rows)},
        "label_sanity_problems": problems,
        "not_found_threshold_from_dev": threshold,
        "lexical_weight_from_dev": best_lw, "dev_mrr_by_lexical_weight": dev_mrr,
        "dev_relevance_scores": dev_scores,
        "retrieval_test": {k: {m: v for m, v in d.items() if m != "top5"} for k, d in retrieval.items()},
        "end_to_end_test": e2e,
        "rows": rows,
        "failures": [r for r in rows if (r["expect"] == "answer" and not r.get("keywords_ok"))
                     or (r["expect"] == "not_found" and r["found"])],
        "hybrid_top5": retrieval[f"hybrid_rrf (dev-tuned {best_lw}:1)"]["top5"],
    }
    res_dir = ROOT / "eval" / "results"
    res_dir.mkdir(parents=True, exist_ok=True)
    (res_dir / f"{tag}.json").write_text(json.dumps(out, indent=2))
    (res_dir / f"{tag}.md").write_text(render_md(out))
    print(render_md(out))
    return 0


def pct(x):
    return "n/a" if x is None else f"{100 * x:.1f}%"


def render_md(o: dict) -> str:
    r, e = o["retrieval_test"], o["end_to_end_test"]
    lines = [
        f"# Evaluation results — `{o['tag']}`",
        "",
        f"Run {o['run_at']} · index `{o['index']['corpus_fingerprint']}` · {o['index']['documents']} documents / "
        f"{o['index']['chunks']} chunks · embedder `{o['index']['embedder']}` · answers `{o['llm_provider']}`",
        f"Test split: {o['queries']['test_answerable']} answerable + {o['queries']['test_out_of_corpus']} out-of-corpus "
        f"questions (dev split of {o['queries']['dev']} used only to tune the not-found threshold = "
        f"{o['not_found_threshold_from_dev']:.2f}; lexical:dense fusion weight = {o['lexical_weight_from_dev']}:1).",
        "",
        "## Retrieval (test split, answerable questions)",
        "",
        "| Retriever | Hit@1 | Recall@5 | Precision@5 | MRR@10 |",
        "|---|---|---|---|---|",
    ]
    for name, d in r.items():
        lines.append(f"| {name} | {pct(d['hit@1'])} | {pct(d['recall@5'])} | {pct(d['precision@5'])} | {d['mrr@10']:.3f} |")
    lines += [
        "",
        "## End to end (test split)",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Answerable questions answered (not wrongly refused) | {pct(e['answerable_answered'])} |",
        f"| Out-of-corpus questions correctly refused (\"not found\") | {pct(e['out_of_corpus_refused'])} |",
        f"| Answer contains the key fact | {pct(e['answer_contains_key_fact'])} |",
        f"| Answer cites a relevant document | {pct(e['answer_cites_relevant_doc'])} |",
        f"| Groundedness (answers whose claims are supported by their citations) | {pct(e['groundedness_rate'])} |",
        f"| Every answer carries a citation | {'yes' if e['every_answer_cited'] else 'NO'} |",
        f"| Latency p50 / p95 | {e['latency_ms_p50']:.0f} ms / {e['latency_ms_p95']:.0f} ms |",
        "",
        "## Failures",
        "",
    ]
    if not o["failures"]:
        lines.append("None.")
    for f in o["failures"]:
        lines.append(f"- `{f['id']}` expected **{f['expect']}**, found={f['found']}, cited={f['citations']}")
    if o["label_sanity_problems"]:
        lines += ["", "## Label sanity problems", ""] + [f"- {p}" for p in o["label_sanity_problems"]]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
