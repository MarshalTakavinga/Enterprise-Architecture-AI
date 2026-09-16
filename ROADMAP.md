# Portfolio Roadmap

Recommended build sequence for the [Enterprise Architecture + AI Portfolio](README.md), with the reasoning behind the order and the flagship selection. Full detail (including per-project effort estimates and skills demonstrated) is in `EA-AI-Portfolio-Blueprint.md` / `.docx`, Step 3.

## Build Sequence

| Order | Project | Difficulty | Est. Effort | Portfolio Value |
|---|---|---|---|---|
| 1 | [EA Knowledge Assistant](01-ea-knowledge-assistant/README.md) | Beginner | 1–2 weeks | Establishes the core retrieval primitive (RAG) everything else reuses |
| 2 | [App Portfolio Redundancy Detector](02-app-portfolio-redundancy-detector/README.md) | Beginner | 1–2 weeks | Shows AI applied to a concrete APM problem, not just Q&A |
| 3 | [ADR Copilot](03-adr-copilot/README.md) | Intermediate | 2 weeks | Demonstrates reliable structured extraction — a distinct, harder skill than open-ended generation |
| 4 | [Technology Lifecycle & EOL Risk Radar](04-tech-lifecycle-risk-radar/README.md) | Intermediate | 2 weeks | Strong "AI judgment" talking point — knowing where *not* to use AI |
| 5 | [Dependency Knowledge Graph & Impact Analyzer](05-ea-dependency-graph/README.md) | Intermediate | 3 weeks | The technical centerpiece later projects build on |
| 6 | [Solution Architecture Compliance Checker](06-solution-compliance-checker/README.md) | Advanced | 2–3 weeks | Bridges the core primitives to real governance workflows |
| 7 | [M&A Architecture Due Diligence Assistant](07-ma-architecture-due-diligence/README.md) | Advanced | 2–3 weeks | A distinctive, memorable interview story most candidates won't have |
| 8 | [AI-Augmented Rationalization & Modernization Roadmap Advisor](08-ai-rationalization-roadmap-advisor/README.md) | **Flagship** | 3–4 weeks | Speaks directly to CIO/CTO-level value — strongest business-value story |
| 9 | [Agentic Architecture Review Board Copilot](09-agentic-arb-copilot/README.md) | **Flagship** | 4–5 weeks | The richest demonstration of modern AI-agent technique, fully governed |
| 10 | [Enterprise Architecture Intelligence Platform (capstone)](10-ea-intelligence-platform/README.md) | **Flagship** | 4–6 weeks | Proves systems thinking — integrates every prior project around one architecture |

**Why this order:** Projects 1–2 are independent and teachable in parallel — they establish the two AI primitives (retrieval, similarity) everything else depends on. Project 3 introduces structured-output reliability. Project 4 is placed deliberately mid-sequence as an early, clear example of *not* over-using AI. Project 5's knowledge graph is the heaviest lift before the flagships, sequenced right before them because Projects 6, 8, 9, and 10 all consume it. Projects 6–7 apply the now-mature primitives to two judgment-heavy governance workflows. The three flagships close the sequence in order of integration complexity.

## Flagship Selection

Three flagships, each demonstrating a different axis of EA + AI capability:

1. **[AI-Augmented Application Rationalization & Modernization Roadmap Advisor](08-ai-rationalization-roadmap-advisor/README.md)** — the *business-value* flagship. Explainable scoring, defensible recommendations, a roadmap a steering committee could act on.
2. **[Agentic Architecture Review Board Copilot](09-agentic-arb-copilot/README.md)** — the *technical-depth* flagship. The richest single demonstration of modern AI technique (multi-agent orchestration, tool calling, RAG, knowledge-graph integration) inside a real governance workflow.
3. **[Enterprise Architecture Intelligence Platform](10-ea-intelligence-platform/README.md)** — the *systems-thinking* flagship. Proves the portfolio is one coherent point of view, not ten disconnected demos.

**First flagship to build:** Project 9, the **Agentic Architecture Review Board Copilot**. It's the single project that legitimately exercises the widest range of AI techniques (LLM, RAG, embeddings, semantic search, knowledge graphs, structured outputs, multi-agent tool/function calling) inside one coherent, governable workflow, and it sits at the architectural center of the capstone (Project 10 largely wraps Project 9's pattern around the other components). Its complete 25-part implementation blueprint — requirements, personas, C4 diagrams, RAG/agent architecture, data model, API design, security, governance, evaluation, milestones, and deployment — is in `EA-AI-Portfolio-Blueprint.md` / `.docx`, Step 4.

## Progress Tracker

Use this to track your own build progress:

- [ ] 1. EA Knowledge Assistant
- [ ] 2. App Portfolio Redundancy Detector
- [ ] 3. ADR Copilot
- [ ] 4. Technology Lifecycle & EOL Risk Radar
- [ ] 5. Dependency Knowledge Graph & Impact Analyzer
- [ ] 6. Solution Architecture Compliance Checker
- [ ] 7. M&A Architecture Due Diligence Assistant
- [ ] 8. AI-Augmented Rationalization & Modernization Roadmap Advisor (Flagship)
- [ ] 9. Agentic Architecture Review Board Copilot (Flagship)
- [ ] 10. Enterprise Architecture Intelligence Platform (Flagship / Capstone)
