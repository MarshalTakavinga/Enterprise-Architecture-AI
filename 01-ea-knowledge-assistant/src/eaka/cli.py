"""Command line: ``eaka ingest`` | ``eaka ask "question"`` | ``eaka docs``."""
from __future__ import annotations

import argparse
import json
import sys


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="eaka", description="EA Knowledge Assistant")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("ingest", help="(Re)build the index from data/corpus")
    a = sub.add_parser("ask", help="Ask a question")
    a.add_argument("question")
    a.add_argument("--provider", default=None, help="extractive | anthropic | azure_openai | openai")
    a.add_argument("--json", action="store_true")
    sub.add_parser("docs", help="List indexed documents")
    sub.add_parser("check", help="Check the configured LLM provider: settings, key, and one test call")
    args = p.parse_args(argv)

    if args.cmd == "ingest":
        from .engine import build_index
        print(json.dumps(build_index(), indent=2))
        return 0

    if args.cmd == "check":
        return check()

    from .engine import KnowledgeAssistant
    ka = KnowledgeAssistant()
    if args.cmd == "docs":
        for d in sorted(ka.documents.values(), key=lambda d: d["doc_id"]):
            print(f"{d['doc_id']:<12} {d['doc_type']:<22} {d['title']}")
        return 0

    ans = ka.ask(args.question, user="cli", provider=args.provider)
    if args.json:
        print(json.dumps(ans.to_dict(), indent=2, ensure_ascii=False))
        return 0
    print(ans.answer)
    if ans.error:
        return 1
    if ans.governance_notice:
        print(f"\n⚠ {ans.governance_notice}")
    if ans.citations:
        print("\nSources:")
        for c in ans.citations:
            print(f"  [{c.n}] {c.doc_id} {c.section_ref} — {c.title}")
    print(f"\n({ans.provider}, {ans.latency_ms} ms, grounded={ans.grounded})")
    return 0


KEYS = {
    "anthropic": ["ANTHROPIC_API_KEY"],
    "openai": ["OPENAI_API_KEY"],
    "azure_openai": ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"],
}


def check() -> int:
    """Print what will be used and make one tiny call, so problems show up before a demo."""
    import os
    import time

    from .answer import generate, resolve_model
    from .config import get_settings
    from .models import Chunk, ScoredChunk

    s = get_settings()
    print(f"{'EAKA_LLM_PROVIDER':<24}: {s.llm_provider}")
    if s.llm_provider == "extractive":
        print("No LLM configured (offline extractive mode). Set EAKA_LLM_PROVIDER to anthropic, azure_openai or openai.")
        return 0
    if s.llm_provider not in KEYS:
        print(f"Unknown EAKA_LLM_PROVIDER '{s.llm_provider}'. Use anthropic, azure_openai or openai.")
        return 1
    missing = []
    for k in KEYS[s.llm_provider]:
        v = os.environ.get(k, "")
        shown = (v[:6] + "…" + v[-4:]) if "KEY" in k and len(v) > 12 else (v or "")
        print(f"{k:<24}: {shown if v else 'MISSING'}")
        if not v:
            missing.append(k)
    if s.llm_provider == "azure_openai" and os.environ.get("AZURE_OPENAI_ENDPOINT"):
        mode = (f"AzureOpenAI client, api-version {os.environ['AZURE_OPENAI_API_VERSION']}"
                if os.environ.get("AZURE_OPENAI_API_VERSION") else "v1 endpoint (<resource>/openai/v1/)")
        print(f"Azure API mode          : {mode}")
    if missing:
        print(f"\nFAIL: set {', '.join(missing)} (in .env or as environment variables).")
        return 1
    try:
        print(f"Model / deployment      : {resolve_model(s.llm_provider, s.llm_model)}")
        src = [ScoredChunk(chunk=Chunk("TEST-1#1", "TEST-1", "Connectivity test", "standard", "§1 Test",
                                       "The connectivity test passphrase is harbour-green."), score=1.0)]
        t0 = time.perf_counter()
        out = generate(s.llm_provider, "What is the connectivity test passphrase?", src, s.llm_model, 200)
        ms = int((time.perf_counter() - t0) * 1000)
    except Exception as e:  # noqa: BLE001
        print(f"\nFAIL: {type(e).__name__}: {e}")
        return 1
    print(f"\nReply ({ms} ms): {out.strip()[:200]}")
    ok = "harbour-green" in out.lower()
    print("OK — the LLM answered from the source and cited it." if ok and "[1]" in out
          else "WARNING: call succeeded but the reply didn't quote/cite the test source as expected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
