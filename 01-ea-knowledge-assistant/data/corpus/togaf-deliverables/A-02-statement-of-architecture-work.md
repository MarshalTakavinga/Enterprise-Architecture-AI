---
doc_id: A-02
title: Statement of Architecture Work — Shipment Platform Consolidation
doc_type: togaf_deliverable
togaf_phase: A
version: "1.0"
status: Approved
owner: David Okafor, Chief Architect
approved_by: Elena Marsh, CIO (signed 2024-12-02; ARB-2024-061)
effective_date: 2024-12-02
next_review: 2025-12-02
classification: Internal
related: [PRE-02, A-01, A-03, A-04, GOV-01, ADD-01, ARS-01, F-01, G-01, AP-03, AP-07, AP-08]
---

# A-02 — Statement of Architecture Work — Shipment Platform Consolidation

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Purpose

This Statement of Architecture Work (SoAW) is the agreement between the Enterprise Architecture Office and the Horizon 2028 sponsor on what architecture work will be done for the Shipment Platform Consolidation, how, by whom, by when, and how the results will be accepted. It converts the Request for Architecture Work PRE-02 and the Architecture Vision A-01 into a controlled engagement governed under GOV-01.

## 2. Background

Harbourline operates three transport management systems — FreightMaster TMS (APP-020), Nordhaven TMS (APP-021) and the FreightMaster Rotterdam instance (a 2019 fork of APP-020 used by Harbourline Europe) — linked by MuleSoft flows and database links. PRE-02, raised by Elena Marsh on 2024-10-07, asked the EA Office to define a single target shipment platform able to support the Horizon 2028 goals approved by the Board in November 2024. A-01 describes the vision, KPIs and transition architectures at summary level. This SoAW commits the resources to take that vision through Phases B to F and to govern delivery through Phases G and H.

## 3. Scope of the Architecture Work

### 3.1 Breadth

Business units: Ocean & Air Forwarding, Customs Brokerage, and the customer-facing parts of Harbourline Digital. Legal entities: all five (Harbourline Inc., Harbourline Canada Ltd., Harbourline Europe B.V., Nordhaven Freight GmbH, Harbourline Gulf FZE).

Port & Terminal Services and Contract Logistics are in scope only at their interfaces with HSP (terminal events, warehouse handoffs).

### 3.2 Depth

| Domain | Depth |
|---|---|
| Business | Level 2 capabilities and value streams for "Quote to Cash (Freight)" and "Shipment Execution"; process models only where regional variants differ |
| Data | Logical data model for shipment, consignment, milestone, carrier, rate; system-of-record assignment; residency placement |
| Application | Logical components of HSP, interfaces with SAP, Salesforce, Customs Filing Gateway, Navis N4, Harbourline Connect |
| Technology | Hosting pattern, regions, resilience tier, integration platform; physical design delegated to solution architects under RA-01 and RA-02 |

### 3.3 Time Horizon

Baseline as at 2024-10-01. Target state Q4 2027. Three transition architectures (TA1 November 2025, TA2 Q2 2027, TA3 Q4 2027), detailed in F-01.

### 3.4 Architecture Domains Excluded

Terminal operating system replacement, warehouse management, CRM platform selection and SAP S/4HANA internal changes.

## 4. Architecture Approach and Tailored ADM

The engagement follows Harbourline's tailored ADM as defined in GOV-01:

| Phase | Tailoring for this engagement |
|---|---|
| Preliminary | Reuse existing principles AP-01..AP-16 and the ARB charter; no new framework work |
| A | This SoAW, A-01, A-03, A-04 |
| B, C, D | Run as one combined iteration producing ADD-01 and ARS-01; Data and Application run in parallel |
| E, F | Opportunities and migration planning merged into one roadmap document, F-01 |
| G | Architecture Contract (G-01) with the delivery partner; compliance assessments at each release gate |
| H | Change requests via `CR-YYYY-NNN`; impact assessed against ARS-01 |

Architecture decisions made during the engagement are recorded as ADRs and approved by the ARB. The repository steward, Samuel Adeyemi, maintains all artefacts in the architecture repository. Reference architectures RA-01, RA-02 and RA-04 will be produced or updated as reusable outputs; the "Reuse, then Buy, then Build" principle (AP-03) will be applied explicitly in the Phase C options analysis.

## 5. Roles and Responsibilities

| Role | Name | Responsibilities |
|---|---|---|
| Executive Sponsor | Elena Marsh, CIO | Funds the work; resolves escalations; signs acceptance |
| Architecture Lead | David Okafor, Chief Architect | Accountable for all architecture deliverables; chairs ARB |
| Programme Director | Grace Liu | Aligns architecture with delivery plan and budget |
| Integration Architecture | Amara Osei | Integration, API and event design |
| Data Architecture | Lena Vogel | Data model, system-of-record, residency |
| Cloud Architecture | Kenji Watanabe | Hosting, resilience, landing zone |
| Security Architecture | Priya Raman | Security architecture and threat modelling |
| Network & OT Architecture | Tomasz Nowak | Terminal interfaces, network |
| Data Protection | Marieke de Vries, DPO | Reviews residency and transfer decisions |
| Business representatives | Michael Torres; regional forwarding heads | Validate capabilities, processes and KPIs |
| Repository Steward | Samuel Adeyemi | Version control, document approval workflow |

RACI for deliverables:

| Deliverable | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| ADD-01 | Domain architects | David Okafor | Business reps, Grace Liu | Steering committee |
| ARS-01 | Domain architects | David Okafor | Priya Raman, Marieke de Vries | Delivery partner |
| F-01 | Grace Liu, David Okafor | Elena Marsh | Rachel Kim | All stakeholders |
| G-01 | David Okafor | Elena Marsh | Delivery partner | ARB |

## 6. Deliverables

| ID | Deliverable | Phase | Due |
|---|---|---|---|
| A-01 | Architecture Vision | A | 2024-11-28 (done) |
| A-03 | Stakeholder Map & Communications Plan | A | 2024-12-13 |
| A-04 | Business Capability Assessment | A/B | 2025-01-24 |
| ADD-01 | Architecture Definition Document | B-D | 2025-03-28 |
| ARS-01 | Architecture Requirements Specification | B-D | 2025-03-28 |
| F-01 | Architecture Roadmap & Migration Plan | E-F | 2025-05-09 |
| G-01 | Architecture Contract — HSP Delivery Programme | G | 2025-05-30 |
| — | ADRs for key decisions | B-D | As raised |

## 7. Work Plan by Phase

| Phase | Start | End | Key activities | Gate |
|---|---|---|---|---|
| A | 2024-10-14 | 2024-12-13 | Vision, stakeholder analysis, capability assessment kickoff | SoAW signed |
| B | 2025-01-06 | 2025-02-21 | Capability map, value streams, regional process variants | ARB checkpoint |
| C (Data) | 2025-01-20 | 2025-03-14 | Logical data model, SoR matrix, residency placement | ARB checkpoint |
| C (Application) | 2025-01-20 | 2025-03-14 | HSP component model, interface catalogue | ARB checkpoint |
| D | 2025-02-17 | 2025-03-28 | Hosting, integration, resilience | ADD-01 / ARS-01 approval |
| E/F | 2025-03-31 | 2025-05-09 | Work packages WP-01..WP-10, transition architectures, costed plan | F-01 approval |
| G | 2025-05-12 | 2027-12-31 | Contract, compliance reviews at each release | Per release |
| H | Continuous | — | Change requests, periodic vision refresh | Quarterly |

Effort estimate: 1,850 architect-days across FY2025, of which 60% internal and 40% from the delivery partner's architects.

## 8. Risks to the Architecture Work

| Risk | Impact | Mitigation |
|---|---|---|
| Business SMEs unavailable during peak season freeze | Phase B slips | Workshops scheduled before mid-October and after mid-January; recorded interviews |
| Nordhaven documentation incomplete | Data model errors | Reverse-engineer from MongoDB Atlas collections; Nordhaven SMEs retained to 2026 |
| Scope creep into warehouse management | Delay and budget overrun | Changes to scope only via change request approved by sponsor |
| Architects pulled into delivery firefighting | Deliverables late | Ring-fenced allocation agreed with Grace Liu |
| Delivery partner selection delayed | G-01 late | Draft contract terms prepared during Phase D |

## 9. Acceptance Criteria and Procedures

### 9.1 Criteria

A deliverable is accepted when:

1. It addresses the scope in §3 for its phase, with no open "TBD" items affecting target-state decisions.
2. Every target component is traceable to at least one goal in A-01 and one requirement in ARS-01.
3. It complies with principles AP-01..AP-16 and current standards, or records the deviation as an exception under GOV-01.
4. Residency and cross-border implications have been reviewed by the DPO.
5. Security architecture has been reviewed by Priya Raman or delegate.
6. KPIs in A-01 have a defined data source and owner.

### 9.2 Procedure

1. The responsible architect submits the deliverable to the repository steward at least five working days before the Thursday ARB session.
2. The ARB reviews and records one of: Approved, Approved with Conditions, Changes Requested, Rejected.
3. Conditions must be closed within 20 working days and are tracked in the ARB log.
4. Phase-closing deliverables (ADD-01, ARS-01, F-01) additionally require sponsor sign-off.
5. Accepted deliverables are baselined in the repository with a version number and become the reference for compliance assessments.

## 10. Sign-off

| Role | Name | Signature | Date |
|---|---|---|---|
| Executive Sponsor | Elena Marsh, CIO | Signed | 2024-12-02 |
| Chief Architect | David Okafor | Signed | 2024-12-02 |
| Programme Director | Grace Liu | Signed | 2024-12-02 |
| CFO (budget) | Rachel Kim | Signed | 2024-12-02 |

## 11. Document History

| Version | Date | Author | Change |
|---|---|---|---|
| 0.8 | 2024-11-15 | David Okafor | Draft |
| 1.0 | 2024-12-02 | Samuel Adeyemi | Signed baseline |
