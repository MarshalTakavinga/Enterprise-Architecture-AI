"""Streamlit chat UI.   streamlit run app/streamlit_app.py

Runs the engine in-process by default; set EAKA_API_URL to call the FastAPI backend instead.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

st.set_page_config(page_title="EA Knowledge Assistant", page_icon="🏛️", layout="wide")

API_URL = os.environ.get("EAKA_API_URL")
EXAMPLES = [
    "What's our approved pattern for asynchronous integration between domains?",
    "Are we allowed to use a NoSQL database for a new service?",
    "Where must EU customer personal data be stored?",
    "What RTO and RPO apply to terminal operations systems?",
    "Can operational technology networks at the terminals reach the internet directly?",
    "Why did we choose Confluent Cloud over Azure Event Hubs?",
    "What is the status of the Nordhaven TMS exception?",
    "What is our mainframe modernisation standard?",
]


@st.cache_resource(show_spinner="Loading the architecture repository index…")
def engine():
    from eaka.engine import KnowledgeAssistant
    return KnowledgeAssistant()


def ask(q: str) -> dict:
    if API_URL:
        import httpx
        headers = {"X-API-Key": os.environ["EAKA_API_KEY"]} if os.environ.get("EAKA_API_KEY") else {}
        return httpx.post(f"{API_URL}/ask", json={"question": q}, headers=headers, timeout=60).json()
    return engine().ask(q, user="streamlit").to_dict()


def feedback(qid: str, ok: bool) -> None:
    if API_URL:
        import httpx
        httpx.post(f"{API_URL}/feedback", json={"query_id": qid, "correct": ok}, timeout=10)
    else:
        engine().log.record_feedback(qid, ok, user="streamlit")


with st.sidebar:
    st.header("Harbourline EA Knowledge Assistant")
    st.caption("Cited answers from the architecture repository — principles, standards, ADRs, "
               "reference architectures and TOGAF deliverables. **Synthetic data; fictional company.**")
    if not API_URL:
        m = engine().meta
        st.metric("Documents indexed", m.get("documents"))
        st.caption(f"{m.get('chunks')} chunks · embedder `{m.get('embedder')}` · index `{m.get('corpus_fingerprint')}`")
        st.caption(f"Answer mode: `{engine().s.llm_provider}`")
    st.divider()
    st.subheader("Try asking")
    for ex in EXAMPLES:
        if st.button(ex, use_container_width=True):
            st.session_state["pending"] = ex
    st.divider()
    st.caption("This assistant answers only from indexed documents and says so when it can't. "
               "It does not author standards or decide exceptions — the ARB does.")

st.session_state.setdefault("history", [])
q = st.chat_input("Ask about a principle, standard, ADR or reference architecture…")
q = q or st.session_state.pop("pending", None)
if q:
    with st.spinner("Searching the repository…"):
        st.session_state["history"].append(ask(q))

for i, a in enumerate(reversed(st.session_state["history"])):
    with st.chat_message("user"):
        st.write(a["question"])
    with st.chat_message("assistant"):
        if a.get("governance_notice"):
            st.warning(a["governance_notice"], icon="⚖️")
        (st.markdown if a["found"] else st.info)(a["answer"])
        if a["citations"]:
            with st.expander(f"Sources ({len(a['citations'])})", expanded=False):
                for c in a["citations"]:
                    st.markdown(f"**[{c['n']}] {c['doc_id']} {c['section_ref']}** — {c['title']}")
                    st.caption(c["quote"])
        cols = st.columns([1, 1, 8])
        grounded = "✅ grounded" if a.get("grounded") else ("—" if a.get("grounded") is None else "⚠ check citations")
        cols[2].caption(f"{a['provider']} · {a['latency_ms']} ms · {grounded}")
        if a.get("query_id"):
            if cols[0].button("👍", key=f"up{i}"):
                feedback(a["query_id"], True); st.toast("Thanks — logged for the evaluation set")
            if cols[1].button("👎", key=f"down{i}"):
                feedback(a["query_id"], False); st.toast("Thanks — logged for review")
