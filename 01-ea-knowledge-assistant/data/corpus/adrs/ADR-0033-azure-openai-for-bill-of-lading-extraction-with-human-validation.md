---
doc_id: ADR-0033
title: Azure OpenAI for Bill of Lading Extraction with Human Validation
doc_type: adr
version: "1.0"
status: Accepted
owner: Lena Vogel, Lead Data Architect
approved_by: Architecture Review Board (ARB-2025-041)
effective_date: 2025-11-04
next_review: 2026-11-04
classification: Internal
related: [AP-02, AP-03, AP-06, AP-16, STD-AI-013, STD-DAT-004, STD-DAT-005, STD-OBS-010, STD-SEC-009, APP-130, APP-060, APP-022]
---

# ADR-0033 — Azure OpenAI for Bill of Lading Extraction with Human Validation

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Status

| Field | Value |
|---|---|
| Status | Accepted |
| Date | 2025-11-04 |
| ARB decision | ARB-2025-041 (session of Thursday 2025-10-30), Approved with Conditions |
| Deciders | David Okafor (Chair), Priya Raman, Lena Vogel, Amara Osei, Kenji Watanabe |
| Consulted | Marieke de Vries (DPO), Hannah Brennan (CISO), Customs Brokerage operations leads (US, NL, DE) |
| Review tier | Tier 1 (AI use case, Restricted data, customs impact) |
| AI Use Case Register | AIU-004, risk tier: High (customs-relevant output) |

## 2. Context

Harbourline's customs and documentation teams receive about 14,000 bills of lading (B/Ls) and associated documents per week as PDFs and scans, in over 300 carrier and forwarder layouts. Staff re-key 35-60 fields per document (parties, container and seal numbers, HS codes, weights, ports) into FreightMaster, HSP and the Customs Filing Gateway (APP-060). Average handling time is 7.5 minutes per document; keying error rate from a 2025 audit is 2.8% of documents with at least one material error. Customs errors lead to holds, amendments and, for EU ICS2 and US ACE filings, possible penalties.

A template-based OCR trial in 2023 was abandoned (<70% accuracy on unseen layouts). STD-AI-013 v1.0 (effective 2025-10-01) now provides the rules for generative AI use. B/Ls with named individuals are personal data and, when they form part of customs declarations, are classified Restricted under STD-DAT-004.

## 3. Decision Drivers

1. Field-level extraction accuracy ≥ 95% on customs-critical fields across unseen layouts.
2. Data stays in the jurisdiction of origin (AP-06, STD-DAT-005, STD-AI-013 in-region rule).
3. A named human is accountable for every customs-relevant output (AP-16).
4. Auditability: prompts, responses and validator actions retained.
5. Handling-time reduction of at least 50%.
6. Use approved platforms before building (AP-03).

## 4. Considered Options

- **Option A — Azure AI Document Intelligence (layout + prebuilt models) with Azure OpenAI (GPT-4o class) for field normalisation**, deployed in-region, with mandatory human validation of customs-relevant fields.
- **Option B — Specialist SaaS document-capture vendor** with its own hosted models (US-hosted processing).
- **Option C — Custom-trained extraction models only** (Document Intelligence custom models per layout family), no LLM.

### 4.1 Comparison

Accuracy figures come from a 1,200-document blind test set (Aug-Sep 2025).

| Criterion | A — DocIntel + Azure OpenAI | B — SaaS vendor | C — Custom models only |
|---|---|---|---|
| Customs-critical field accuracy | 96.8% | 95.1% | 91.4% (drops on unseen layouts) |
| Data residency | In-region (East US 2, West Europe, UAE North) | US processing; TIA and SCCs needed | In-region |
| Approved platform (STD-AI-013) | Yes | No; would need new vendor assessment | Yes |
| Cost per document (est.) | USD 0.09 | USD 0.35 | USD 0.04 + labelling effort |
| Build effort | ~5 months, 4 engineers | ~3 months integration | ~8 months incl. labelling 6,000 docs |
| Explainability for validators | Bounding boxes + confidence per field | Confidence only | Bounding boxes + confidence |

## 5. Decision Outcome

**Chosen option: A — Azure AI Document Intelligence plus in-region Azure OpenAI, delivered as DocIntel (APP-130), with human validation.**

Conditions from ARB-2025-041:

1. **Human in the loop:** a trained validator MUST confirm every customs-relevant field (parties, HS codes, container and seal numbers, weights, package counts, ports) before data is written to HSP or the Customs Filing Gateway. No auto-submission to customs authorities. Non-customs fields with confidence ≥ 0.98 may be auto-accepted.
2. **Accountability:** the validator's identity is stored with each confirmed record; the Head of Customs Brokerage for each region is the accountable owner for AIU-004.
3. **Residency:** documents are processed in the region of the receiving entity (West Europe for Harbourline Europe and Nordhaven, East US 2 for Harbourline Inc., UAE North for Harbourline Gulf, Canada Central for Harbourline Canada). No cross-region fallback without DPO approval.
4. **Security:** private endpoints only; customer-managed keys in Key Vault Premium for stored documents; abuse-monitoring data handling approved by the DPO.
5. **Logging:** prompts and responses retained 90 days in a restricted Log Analytics workspace; no document content in general application logs (STD-OBS-010).
6. **Model changes:** any change of model version requires re-running the blind test set; accuracy on customs-critical fields must not fall below 95%.
7. **EU AI Act:** assessment completed by Lena Vogel and the DPO before EU go-live.

## 6. Consequences

### 6.1 Positive

- Pilot shows handling time falling from 7.5 to 2.9 minutes per document (61% reduction), equivalent to ~26 FTE of capacity redeployed across regions.
- Validators correct fewer errors than they key today; the pilot's material error rate was 0.6%.
- Uses approved platforms and in-region processing with no new vendor.

### 6.2 Negative

- Human validation caps the achievable saving; full automation is explicitly out of scope and will stay so while customs output is involved.
- Azure OpenAI capacity in some approved regions is constrained; UAE North provisioned throughput required a 10-week quota request.
- Risk of automation bias: validators may confirm fields without checking. Mitigated by weekly sampling of 2% of confirmed documents and seeded test documents.
- Model versions are retired by the provider on its own schedule, forcing re-validation work roughly every 9-12 months.
- Running cost ~USD 65k/year plus 1 FTE for model evaluation and prompt maintenance.

### 6.3 Neutral

- Reusable for other document types, each needing its own AIU registration.

### 6.4 Follow-up actions

| Action | Owner | Due |
|---|---|---|
| Update AIU-004 entry with risk tier and controls | Lena Vogel | 2025-11-14 |
| Validator training and sampling procedure | Customs Brokerage leads | 2025-12-15 |
| EU AI Act assessment for EU deployment | Lena Vogel / Marieke de Vries | 2026-01-31 |
| Accuracy and override-rate dashboard | Kenji Watanabe | 2026-01-31 |

## 7. Compliance with Principles & Standards

| Reference | Assessment |
|---|---|
| AP-16 Accountable Use of AI | Compliant; named validator and accountable owner. |
| STD-AI-013 | Approved platform, registered use case, human review for customs decisions, 90-day prompt logs. |
| AP-06 / STD-DAT-005 | In-region processing per entity. |
| STD-DAT-004 / STD-SEC-009 | Restricted data under CMK, private endpoints, PIM access. |
| AP-02 Compliance by Design | Customs filing controls preserved. |

## 8. Links

- APP-130 DocIntel — Bill of Lading Extraction (AIU-004)
- STD-AI-013 AI & Generative AI Usage Standard
- APP-060 Customs Filing Gateway
- ARB log entry ARB-2025-041
