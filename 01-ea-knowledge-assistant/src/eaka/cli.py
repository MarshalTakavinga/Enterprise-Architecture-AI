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
    args = p.parse_args(argv)

    if args.cmd == "ingest":
        from .engine import build_index
        print(json.dumps(build_index(), indent=2))
        return 0

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
    if ans.governance_notice:
        print(f"\n⚠ {ans.governance_notice}")
    if ans.citations:
        print("\nSources:")
        for c in ans.citations:
            print(f"  [{c.n}] {c.doc_id} {c.section_ref} — {c.title}")
    print(f"\n({ans.provider}, {ans.latency_ms} ms, grounded={ans.grounded})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
