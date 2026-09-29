---
doc_id: G-01
title: Architecture Contract — HSP Delivery Programme
doc_type: togaf_deliverable
togaf_phase: G
version: "1.1"
status: Active
owner: Samuel Adeyemi, Head of Enterprise Architecture Office / ARB Secretary
approved_by: Architecture Review Board (ARB-2025-006)
effective_date: 2025-02-06
next_review: 2027-02-04
classification: Confidential
related: [GOV-01, GOV-02, A-02, ADD-01, ARS-01, F-01, AP-07, AP-08, AP-12, AP-14, AP-15, STD-INT-001, STD-API-002, STD-EVT-003, STD-DAT-004, STD-DAT-005, STD-DB-006, STD-CLD-007, STD-IAM-008, STD-SEC-009, STD-OBS-010, STD-CTR-012, STD-RES-015, STD-AI-013]
---

# G-01 — Architecture Contract — HSP Delivery Programme

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This contract records the binding agreement between the Enterprise Architecture Office and the Harbourline Shipment Platform (HSP) delivery programme on how the target architecture in ADD-01 will be realised. It sets out what the programme will conform to, how conformance is checked, how deviations are handled and how success is measured. It is referenced in the statement of work between Harbourline Inc. and Kestrel Digital Partners, so obligations below apply to Kestrel personnel working on HSP.

## 2. Parties

| Party | Represented by | Role in this contract |
|---|---|---|
| Enterprise Architecture Office | Samuel Adeyemi, Head of EA Office | Architecture authority; maintains repository and compliance records |
| Architecture Review Board | David Okafor, Chief Architect and ARB Chair | Approves designs, deviations and exceptions |
| HSP Delivery Programme | Grace Liu, Programme Director | Accountable for delivering HSP to this contract |
| Kestrel Digital Partners (systems integrator) | Kestrel Engagement Director and Kestrel Lead Architect | Designs and builds HSP services under Harbourline direction |
| Executive sponsor | Elena Marsh, CIO | Arbitrates unresolved disputes |

## 3. Scope

In scope: all HSP services (APP-022), their infrastructure, integrations with the Event Backbone (APP-120) and API Gateway (APP-121), data migrations from FreightMaster (APP-020) and Nordhaven TMS (APP-021), and the HSP-side of integrations with Harbourline Connect (APP-050), Customs Filing Gateway (APP-060), SAP S/4HANA (APP-010) and Tidewater (APP-080). The scope follows work packages WP-01 to WP-10 in F-01.

Out of scope: changes inside Navis N4 (APP-030) and terminal OT networks, which remain under Port & Terminal Services governance and RA-03.

## 4. Architecture and Standards to Conform To

The programme MUST deliver an architecture consistent with ADD-01 and satisfy the requirements in ARS-01. Specifically:

| Area | Governing documents | Key obligations |
|---|---|---|
| Integration | STD-INT-001, STD-EVT-003, ADR-0038, RA-01 | Domain events via outbox and CDC; no new MuleSoft flows; no cross-domain DB links |
| APIs | STD-API-002, ADR-0019 | OpenAPI 3.1 contracts, published through APIM, OAuth 2.0 via Entra ID |
| Data | STD-DAT-004, STD-DAT-005, STD-DB-006 | Classification tags; EU personal data in West Europe; PostgreSQL Flexible Server default |
| Hosting | STD-CLD-007, STD-CTR-012, RA-02 | Azure landing zone, AKS, signed images from `hlgacr`, Terraform |
| Security | STD-IAM-008, STD-SEC-009 | Managed identities, PIM, customer-managed keys for Restricted data |
| Operations | STD-OBS-010, STD-RES-015 | OpenTelemetry, SLOs, Tier 1 resilience with annual DR test |
| AI | STD-AI-013, ADR-0033 | Registered use cases, human validation of customs fields |

Kestrel Digital Partners MUST NOT introduce products, frameworks or cloud services not rated Adopt or Trial in STD-TLC-014 without ARB approval. Harbourline owns all code, IaC and architecture artefacts produced under this contract; they are stored in Harbourline repositories from the first commit.

## 5. Compliance Checkpoints

| Checkpoint | Timing | Review tier | Evidence required |
|---|---|---|---|
| CP1 Solution design | Before build of each work package | Tier 1 (ARB) | Solution design, data flow with classifications, updated ADD-01 views |
| CP2 Data placement | Before any personal data is loaded to a new region | Tier 1 (ARB, DPO present) | Data inventory, residency mapping to STD-DAT-005, TIA where needed |
| CP3 Pre-production | Before each wave cutover | Tier 2 (two domain architects) | Test results for REQ-HSP-014, -015, -016; penetration test; SLO dashboards |
| CP4 Post-implementation | 60 days after each wave | Tier 2 | Measured latency, incident record, cost versus estimate |
| Ongoing | Every sprint | Tier 3 checklist | Tag compliance, image scan results, IaC drift report |

Compliance assessments are recorded in the ARB log under `ARB-YYYY-NNN` using the format in GOV-01.

## 6. Deviations and Exceptions

1. A team that cannot meet a standard MUST raise the deviation with the EA Office before building the non-conforming solution.
2. The EA Office decides within 5 business days whether the deviation needs an exception or a design change.
3. Exceptions follow the GOV-01 process: maximum 12 months, renewable once, with a remediation plan and a named owner, recorded in GOV-02.
4. Deviations found at a checkpoint without a prior request are logged as non-conformances; two non-conformances in one work package trigger a programme-level review with the CIO.
5. Contract changes to scope or target architecture are made through Phase H change requests (`CR-YYYY-NNN`).

## 7. Measures of Success

| Measure | Target | Source |
|---|---|---|
| Milestone latency | < 5 min p95 (REQ-HSP-014) | Azure Monitor SLO dashboard |
| Tier 1 DR test | Passed annually, RTO ≤ 1 h, RPO ≤ 15 min | DR test report |
| Standards conformance at CP1/CP3 | ≥ 95% of checklist items compliant at first review | ARB log |
| Open exceptions attributable to HSP | ≤ 2 at any time | GOV-02 |
| MuleSoft flows created | 0 | Integration inventory |
| Critical CVEs in production images | 0 | Container scan reports |

## 8. Roles and Responsibilities

- **EA Office:** provides domain architects to each checkpoint; keeps this contract and ADD-01 current.
- **HSP programme:** produces checkpoint evidence; funds remediation of non-conformances.
- **Kestrel Digital Partners:** assigns a Lead Architect accountable for conformance; names key personnel for each squad; gives two weeks' notice of any key-person change.

## 9. Term, Review and Dispute Resolution

This contract is effective from signature until the HSP target state (TA3 in F-01) is formally accepted by the ARB, expected in Q4 2027. The EA Office reviews it annually and whenever ADD-01, ARS-01 or a referenced standard receives a major version change; a new standard version applies to work packages that have not yet passed CP1. Disagreements about the interpretation of a standard are first resolved by the owning domain architect, then by the ARB Chair, and finally by the CIO as executive sponsor.

## 10. Signatures

| Name | Role | Organisation | Date |
|---|---|---|---|
| David Okafor | Chief Architect, ARB Chair | Harbourline Logistics Group | 2025-02-06 |
| Samuel Adeyemi | Head of EA Office | Harbourline Logistics Group | 2025-02-06 |
| Grace Liu | Programme Director, HSP | Harbourline Logistics Group | 2025-02-06 |
| Engagement Director | Kestrel Digital Partners | Kestrel Digital Partners | 2025-02-07 |
| Elena Marsh | CIO (sponsor, acknowledgement) | Harbourline Logistics Group | 2025-02-10 |

## 11. Document History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2025-02-06 | Signed |
| 1.1 | 2026-01-15 | Added AI obligations (STD-AI-013) and CP2 data placement checkpoint |
