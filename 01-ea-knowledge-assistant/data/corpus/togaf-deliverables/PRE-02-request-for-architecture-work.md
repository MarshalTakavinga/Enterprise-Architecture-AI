---
doc_id: PRE-02
title: Request for Architecture Work — Shipment Platform Consolidation
doc_type: togaf_deliverable
togaf_phase: Preliminary
version: "1.0"
status: Approved
owner: Elena Marsh, Chief Information Officer
approved_by: Architecture Review Board (ARB-2024-049)
effective_date: 2024-10-07
next_review: 2025-10-07
classification: Internal
related: [PRE-01, GOV-01, A-01, A-02, AP-03, AP-07, AP-08, ADR-0007, ADR-0015]
---

# PRE-02 — Request for Architecture Work — Shipment Platform Consolidation

> Synthetic document for a portfolio project. Harbourline Logistics Group is a fictional company.

## 1. Request Summary

| Field | Value |
|---|---|
| Request date | 2024-10-07 |
| Sponsor | Elena Marsh, Chief Information Officer |
| Requesting organisation | Group IT, on behalf of Ocean & Air Forwarding, Customs Brokerage and Harbourline Digital |
| Architecture lead requested | David Okafor, Chief Architect |
| Programme | Horizon 2028 (subject to Board approval, November 2024) |
| Review route | Tier 1 — new system, Restricted data, cross-border data, cost > USD 500k (GOV-01 §6) |

## 2. Sponsor and Organisation

The sponsor is the CIO, who will be accountable to the Board for Horizon 2028. The work affects three business units directly (Ocean & Air Forwarding, Customs Brokerage, Contract Logistics & Warehousing) and Port & Terminal Services indirectly through terminal milestone feeds. Nordhaven Freight GmbH, acquired in March 2024, is in scope as an operating entity.

## 3. Description of the Request

Harbourline currently manages shipments in three transport management systems:

- **FreightMaster TMS (APP-020)** — in-house, built 2009, running on Oracle 12c and Java 8 in the Baltimore data centre; used by Harbourline Inc., Harbourline Canada and Harbourline Gulf.
- **Nordhaven TMS (APP-021)** — acquired with Nordhaven; Java 11 with MongoDB Atlas on AWS eu-central-1; used for German and Central European lanes.
- **FreightMaster Rotterdam instance** — a 2019 fork of APP-020 with its own Oracle 12c schema in the Rotterdam server room, used by Harbourline Europe B.V.

Shipment status reaches customers through overnight batch extracts and polling by the portal, typically 2 to 6 hours late. Billing disputes arise from mismatched records across systems.

The sponsor requests architecture work to define a single target shipment platform — provisionally named the Harbourline Shipment Platform (HSP) — together with the transition path that retires the existing systems and enables real-time visibility.

## 4. Objectives

1. Define a target architecture for one cloud-native shipment platform acting as the system of record for shipments (AP-07).
2. Define an event-driven integration approach that publishes shipment milestones to customer-facing channels in near real time (AP-01, AP-08).
3. Produce a sequenced roadmap that retires FreightMaster in time for the Baltimore data centre exit and migrates Nordhaven lanes without service disruption.
4. Identify the standards, platform capabilities and exceptions required, and the architecture decisions to be taken.
5. Provide a cost and benefit baseline sufficient for the CFO to release the first funding tranche.

## 5. Scope

### 5.1 In scope
- Business capabilities: shipment booking, planning, execution, visibility, carrier management, and billing handoff to SAP S/4HANA (APP-010).
- Applications: APP-020 (Baltimore and Rotterdam instances), APP-021, and their interfaces to Salesforce (APP-040), Customs Filing Gateway (APP-060), Harbourline Connect (APP-050) and Navis N4 (APP-030) terminal events.
- Integration: replacement of shipment-related MuleSoft flows; event publication through the Harbourline Event Backbone (APP-120, ADR-0007).
- Data: shipment, booking, party and milestone data, including personal data of consignees.
- Entities: Harbourline Inc., Harbourline Canada Ltd., Harbourline Europe B.V., Nordhaven Freight GmbH, Harbourline Gulf FZE.

### 5.2 Out of scope
- Terminal operating system replacement (Navis N4 remains).
- Warehouse management (Manhattan Active WM, APP-070).
- Finance processes within SAP S/4HANA beyond the billing interface.
- Customs filing logic within APP-060, except its interface to the shipment platform.

## 6. Constraints

- Baltimore data centre exit is fixed at 30 June 2027; FreightMaster must be retired or relocated before then.
- Azure is the primary cloud; any continued use of AWS requires ARB approval.
- EU personal data must remain in the EU.
- No disruption to terminal operations; terminal systems must retain 72-hour autonomy.
- Oracle 12c extended support ends 31 March 2027.
- The MuleSoft contract ends 31 December 2026 and will not be renewed.
- Architecture work must follow the tailored ADM in GOV-01.

## 7. Budget

| Item | Amount |
|---|---|
| Architecture work (Phases A-F), internal EA effort plus external support | USD 1.4M |
| Indicative programme envelope for HSP build and migration (for Phase A validation) | USD 62M of the proposed USD 118M Horizon 2028 budget |

The architecture budget is funded from the CIO's FY2025 transformation reserve. The programme envelope is indicative and will be confirmed in A-02.

## 8. Timeline

| Milestone | Target date |
|---|---|
| Request accepted by ARB | 2024-10-10 |
| Architecture Vision (A-01) approved | 2024-11-28 |
| Statement of Architecture Work (A-02) signed | 2024-12-02 |
| Architecture Definition (ADD-01) and Requirements (ARS-01) baselined | 2025-03-31 |
| Roadmap (F-01) approved | 2025-04-30 |
| First release target (US lanes) | November 2025 |

## 9. Stakeholders

| Stakeholder | Interest |
|---|---|
| Elena Marsh, CIO | Sponsor |
| Grace Liu, Programme Director (designate) | Delivery planning |
| Rachel Kim, CFO | Business case, billing accuracy |
| Michael Torres, VP Port & Terminal Services | Terminal event integration |
| Hannah Brennan, CISO | Security and NIS2 obligations |
| Marieke de Vries, DPO | Personal data and transfers |
| Amara Osei, Lena Vogel, Kenji Watanabe, Priya Raman | Domain architecture |
| Nordhaven operations leadership | Migration impact |

## 10. Success Criteria

- A single target shipment platform architecture approved by the ARB.
- A roadmap demonstrating FreightMaster retirement before 30 June 2027.
- A design capable of 95% of milestone events reaching customers within 5 minutes.
- Residency approach for EU, Canadian and UAE data agreed with the DPO.
- Business case accepted by the CFO for tranche 1 funding.

## 11. Approval

| Role | Name | Decision | Date |
|---|---|---|---|
| Sponsor | Elena Marsh | Submitted | 2024-10-07 |
| ARB Chair | David Okafor | Accepted (ARB-2024-049) | 2024-10-10 |
