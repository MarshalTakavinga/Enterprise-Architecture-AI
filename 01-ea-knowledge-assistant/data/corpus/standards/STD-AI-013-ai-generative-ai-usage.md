---
doc_id: STD-AI-013
title: AI & Generative AI Usage Standard
doc_type: standard
version: "1.0"
status: Approved
owner: Priya Raman, Principal Security Architect & Lena Vogel, Lead Data Architect
approved_by: Architecture Review Board (ARB-2025-071)
effective_date: 2025-10-01
next_review: 2026-10-01
classification: Internal
related: [AP-16, AP-02, AP-05, AP-06, STD-DAT-004, STD-DAT-005, STD-DB-006, STD-SEC-009, STD-IAM-008, STD-OBS-010, STD-CLD-007, STD-TLC-014, GOV-01, GOV-02]
---

# STD-AI-013 — AI & Generative AI Usage Standard

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This standard sets the rules under which Harbourline designs, buys and operates AI systems, including large language models (LLMs) and retrieval-augmented generation (RAG). It puts principle AP-16 (Accountable Use of AI) into practice: every AI-assisted decision has a named accountable human, every use case is registered and risk-tiered, and Harbourline data stays within approved platforms and jurisdictions.

## 2. Scope

### 2.1 In scope

- Any system that uses machine learning, LLMs or generative AI to produce content, classifications, extractions, recommendations or decisions used in Harbourline business processes.
- AI capabilities embedded in purchased SaaS products when they process Harbourline data classified Internal or above.
- Employee and contractor use of external AI tools for work purposes.

### 2.2 Out of scope

- Deterministic rules engines and conventional statistical reporting in Tidewater (APP-080) that do not use trained models.
- Code-completion assistants inside approved developer tooling are covered only by §5 (data handling) and §9 (logging).

## 3. Related Principles & Normative References

| Reference | Relevance |
|---|---|
| AP-16 Accountable Use of AI | A named human is accountable for every AI-assisted decision |
| AP-02 Compliance by Design | EU AI Act, GDPR and sector obligations are assessed before build |
| AP-06 Data Residency Follows Jurisdiction | Model inference stays in the data's region |
| STD-DAT-004 | Classification of prompts, retrieved content and outputs |
| STD-DAT-005 | Regional placement of AI services processing personal data |
| STD-DB-006 | pgvector (Trial) approved for AI retrieval use cases |
| Regulation (EU) 2024/1689 (EU AI Act) | Risk classification for EU-facing use cases |

The key words MUST, MUST NOT, SHOULD, SHOULD NOT and MAY are to be interpreted as described in RFC 2119.

## 4. Approved AI Platforms

| Platform | Radar status | Conditions |
|---|---|---|
| Azure OpenAI Service | Adopt | Deployed in approved regions per STD-CLD-007; regional (non-global) deployments for personal or Restricted data |
| Azure AI Document Intelligence | Adopt | Document extraction |
| Azure AI Search | Adopt | Retrieval index for RAG |
| PostgreSQL pgvector extension | Trial | Retrieval store for RAG where data already lives in PostgreSQL |
| AWS Bedrock | Trial | Nordhaven Freight only, eu-central-1, until HSP migration |
| Public consumer AI tools (free or personal accounts) | Not approved | Public data only (see §5.2) |

1. New AI use cases MUST use Azure OpenAI Service unless the ARB approves an alternative under Tier 1 review.
2. Model deployments MUST be placed in the same region as the data they process. EU personal data MUST be processed by deployments in West Europe or North Europe only; UAE personal data in UAE North; Canadian data in Canada Central or Canada East where contractually required.
3. Global or cross-region model routing options MUST NOT be used for Confidential or Restricted data.
4. Azure OpenAI resources MUST have public network access disabled, be accessed through private endpoints and authenticate with managed identities (STD-IAM-008). API keys MUST be disabled.
5. Abuse-monitoring data handling and content filtering configuration MUST be recorded in the use case's register entry.

## 5. Data Handling

### 5.1 Classification

1. Prompts, retrieved context, fine-tuning data and model outputs MUST be classified at the highest classification of the data they contain (STD-DAT-004).
2. Restricted data MAY be sent to an approved platform only if the use case is registered at risk tier High or Medium, the deployment is regional, and the owning data owner has approved it.
3. Harbourline data MUST NOT be used to fine-tune or train third-party foundation models outside Harbourline's own tenant.

### 5.2 Public consumer AI tools

1. Internal, Confidential and Restricted data MUST NOT be entered into public consumer AI tools, including uploads of files, screenshots, code or email text.
2. Only Public data MAY be used with such tools. Web categories for unapproved AI services are blocked or monitored at the FortiGate breakout per STD-NET-011.

## 6. AI Use Case Register and Risk Tiers

1. Every AI use case MUST be registered in the AI Use Case Register before development starts, with an identifier `AIU-NNN`, a named business owner, a named accountable human decision-maker, the data classes processed, the model and platform, and a risk tier.
2. The register is maintained by the EA Office (Samuel Adeyemi) and reviewed quarterly by the ARB.

| Risk tier | Criteria | Review required |
|---|---|---|
| Low | Internal productivity; no personal data; output reviewed before any external use | Tier 3 self-certification |
| Medium | Customer-facing content, operational recommendations, or personal data processing | ARB Tier 2 review + DPO consultation |
| High | Output influences customs, safety, HR or financial decisions, or Restricted data | ARB Tier 1 review + DPO + CISO sign-off |
| Prohibited | Uses listed as prohibited practices under the EU AI Act, or fully automated decisions with legal effect on individuals | Not permitted |

3. Registered examples include AIU-004 (Bill of Lading extraction, DocIntel APP-130), tiered High because extracted fields feed customs filings.

## 7. Human Oversight

1. For High-tier use cases, a qualified human MUST review and confirm AI output before any action is taken. This includes customs declarations and filings, safety-related terminal decisions, and HR decisions.
2. The review step MUST be enforced in the workflow (for example, a validation queue), not left to user discretion, and MUST record the reviewer's identity and decision.
3. User interfaces MUST clearly indicate AI-generated content and confidence where available.
4. The accountable human named in the register MUST be able to suspend the use case at any time.

## 8. RAG and Output Quality

1. RAG answers MUST cite the source documents or records used, with an identifier the user can open.
2. RAG retrieval MUST enforce the requesting user's access rights; retrieval indexes MUST NOT expose content the user could not otherwise read.
3. Use cases MUST have an evaluation set and documented acceptance thresholds for accuracy and groundedness before production, re-run on every model version change.
4. Systems SHOULD decline to answer when retrieved evidence is insufficient, rather than generate unsupported content.

## 9. Logging and Monitoring

1. Prompts and responses MUST be logged, with user and use-case identifiers, and retained for 90 days in a restricted-access store.
2. Logged prompts containing personal data MUST be stored in the data's home region and access to them MUST be limited to the use case's support team and security operations.
3. AI services MUST emit telemetry per STD-OBS-010, including token usage, latency, content-filter events and error rates.

## 10. EU AI Act and Regulatory Assessment

1. Every EU-facing use case, and any use case processing data of EU data subjects, MUST complete an EU AI Act classification assessment before production, reviewed by the Group DPO, Marieke de Vries.
2. Use cases processing personal data MUST also complete a data protection impact screening under GDPR, PIPEDA or UAE PDPL as applicable.

## 11. Compliance & Exceptions

1. Conformance is assessed through ARB reviews at the tier set in §6, under GOV-01.
2. Deviations MUST follow the GOV-01 exception process and be recorded in GOV-02, with a remediation plan and a maximum duration of 12 months, renewable once. No exception may waive §7.1 human review for High-tier use cases.

## 12. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.9 | 2025-07-15 | Priya Raman, Lena Vogel | Draft for consultation with DPO and CISO |
| 1.0 | 2025-10-01 | Priya Raman, Lena Vogel | First approved issue (ARB-2025-071) |
