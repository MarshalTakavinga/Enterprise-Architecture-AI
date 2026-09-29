# Enterprise Architecture + AI Portfolio

A portfolio of ten realistic, enterprise-grade projects demonstrating how AI, GenAI, LLMs, and AI agents can improve Enterprise Architecture practice — built to be credible in front of a CIO, CTO, Chief Architect, or Architecture Review Board, not a collection of generic AI demos.

**Author:** Marshal Tafadzwa Takavinga — Cloud & Enterprise Architecture practitioner (Azure Solutions Architect Expert, AWS Certified Professional, TOGAF in progress), M.S. Information Systems Technology, George Washington University.

## Start Here

1. Read **`EA-AI-Portfolio-Blueprint.docx`** (or `.md`) — the full blueprint. It contains:
   - An EA-lifecycle-wide assessment of where AI genuinely adds value vs. where automation or human judgment wins
   - The complete specification for all 10 projects below (problem, business value/KPIs, AI use case, architecture, data model, governance, phased plan, evaluation)
   - The prioritized build sequence and the reasoning behind the three flagship projects
   - A full 25-part implementation blueprint (with architecture diagrams) for the first flagship, the Agentic Architecture Review Board Copilot
2. See **`ROADMAP.md`** for the recommended build order and where each project fits.
3. Each numbered subfolder below is a project workspace with its own `README.md` (the same spec, extracted for that project) and a starter folder skeleton (`data/`, `src/`, `app/`, `docs/`, `tests/`, `eval/`) ready to build in.

## The Portfolio

| # | Project | Tier | Folder |
|---|---|---|---|
| 1 | EA Knowledge Assistant (RAG over the Architecture Repository) | Beginner | `01-ea-knowledge-assistant/` |
| 2 | Application Portfolio Semantic Redundancy Detector | Beginner | `02-app-portfolio-redundancy-detector/` |
| 3 | Architecture Decision Record (ADR) Copilot | Intermediate | `03-adr-copilot/` |
| 4 | Technology Lifecycle & EOL Risk Radar | Intermediate | `04-tech-lifecycle-risk-radar/` |
| 5 | Architecture Dependency Knowledge Graph & Impact Analyzer | Intermediate | `05-ea-dependency-graph/` |
| 6 | Solution Architecture Standards Compliance Checker | Advanced | `06-solution-compliance-checker/` |
| 7 | M&A / Divestiture Architecture Due Diligence Assistant | Advanced | `07-ma-architecture-due-diligence/` |
| 8 | AI-Augmented Application Rationalization & Modernization Roadmap Advisor | **Flagship** | `08-ai-rationalization-roadmap-advisor/` |
| 9 | Agentic Architecture Review Board Copilot | **Flagship** | `09-agentic-arb-copilot/` |
| 10 | Enterprise Architecture Intelligence Platform ("AI Command Center") | **Flagship / Capstone** | `10-ea-intelligence-platform/` |

## Design Principles Behind Every Project

- **A human stays accountable for every decision.** AI drafts, classifies, scores, ranks, and surfaces evidence — it never approves an architecture, closes a risk, or finalizes a standard.
- **AI techniques are chosen, not collected.** Every project spec states plainly which techniques are required and which would be over-engineering — including one project (#4) built specifically to demonstrate where deterministic logic beats an LLM.
- **All data is synthetic.** Every project is designed to be prototyped with public, synthetic, or self-generated enterprise data — no confidential corporate systems required.
- **It's one system, not ten demos.** Projects 1–2 establish core AI primitives (retrieval, similarity); 3–5 add structured extraction and graph reasoning; 6–7 apply those to real governance workflows; the three flagships recombine everything into progressively more ambitious systems.

## Folder Structure

```
Portfolio/
├── README.md                          (this file)
├── ROADMAP.md                         (build sequence & flagship rationale)
├── EA-AI-Portfolio-Blueprint.docx     (full blueprint — Word)
├── EA-AI-Portfolio-Blueprint.md       (full blueprint — Markdown, with Mermaid diagram source)
├── 01-ea-knowledge-assistant/
│   ├── README.md
│   └── data/ src/ app/ docs/ tests/ eval/
├── 02-app-portfolio-redundancy-detector/
│   └── ...
├── ...
└── 10-ea-intelligence-platform/
    └── ...
```

## License & Data Disclaimer

All datasets referenced across this portfolio are synthetic and generated for demonstration purposes. No real organizational, customer, or confidential data is used anywhere in this portfolio.
